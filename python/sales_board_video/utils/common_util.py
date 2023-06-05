import pandas as pd
from pandas import DataFrame
import cv2
import json
import os

from collections import defaultdict
import numpy as np

import requests


host_vr = ""

host_koubei = ''

class GetKeyValue(object):
    def __init__(self, o, mode='j'):
        self.json_object = None
        if mode == 'j':
            self.json_object = o
        elif mode == 's':
            self.json_object = json.loads(o)
        else:
            raise Exception('Unexpected mode argument.Choose "j" or "s".')

        self.result_list = []

    def search_key(self, key):
        self.result_list = []
        self.__search(self.json_object, key)
        return self.result_list

    def __search(self, json_object, key):

        for k in json_object:
            if k == key:
                self.result_list.append(json_object[k])
            if isinstance(json_object[k], dict):
                self.__search(json_object[k], key)
            if isinstance(json_object[k], list):
                for item in json_object[k]:
                    if isinstance(item, dict):
                        self.__search(item, key)
        return


def insert_pd(data:DataFrame,fre=2):
    if fre<1:
        return data
    df_new = data
    idx = 0
    for i in range(1,len(data)):
        df1 = df_new.iloc[:(1+(i-1)*(fre+1)),:]
        df2 = df_new.iloc[(1+(i-1)*(fre+1)):,:]
        df_adds = []
        columns = df1.columns
        values_up = df1.iloc[-1:].values
        index_up = df1.iloc[-1:].index
        values_down = df2.iloc[:1].values
        for j in range(fre):
            tmp_value = (values_up+(values_down-values_up)/(fre+1)*(j+1)).tolist()[0]
            index = index_up[0]
            tmp_d = {}
            for idx,column in enumerate(columns):
                tmp_d.update({column:{index:int(tmp_value[idx])}})
            df_add = pd.DataFrame(tmp_d)
            df_adds.append(df_add)
        tmp = []
        tmp.append(df1)
        tmp.extend(df_adds)
        tmp.append(df2)
        df_new = pd.concat(tmp,ignore_index=False)
    return df_new

def get_video_duration(video_file):
    cap = cv2.VideoCapture(video_file)
    frame_num = cap.get(7)
    fps = cap.get(5)
    duration = frame_num/fps
    return duration


def trans(png_duration,video_rows,video_duration):
    for idx,p in enumerate(png_duration):
        max_idx = p[0]
        start = p[1][0]
        end = p[1][1]
        start_time = start/video_rows*video_duration
        end_time = end/video_rows*video_duration
        png_duration[idx][1]=[start_time,end_time]
    return 

def get_png(series_id,series_name,vr_dir):
    if os.path.isfile(f'{vr_dir}/{series_name.replace(" ","")}.png'):
        return
    try:
        response = requests.get(host_vr.format(int(series_id)))
        data = json.loads(response.content)
        vr_img = data['result']['color_list'][0]['Hori']['Normal'][0]['Url']
        with open(f'{vr_dir}/{series_name.replace(" ","")}.png','wb') as f:
            f.write(requests.get(vr_img).content)
    except Exception as e:
        print(e)
        print(f'VR:{series_name} failed')

def get_koubei(res_df_sum_new:DataFrame,series_name_id:dict):
    '''
        d_tmp:{
            
            series_name:{
                'sale_num':100,
                'series_id':5000,
                'user_name':a,
                'price':20,
                'advantage':...,
                'short_coming':
            }
        
        }
    '''
    sale_nums = res_df_sum_new.iloc[-1:].values.tolist()[0]
    series_names = res_df_sum_new.iloc[-1:].columns.tolist()
    d_tmp = defaultdict(dict)
    for idx,sn in enumerate(series_names):
        if sn.startswith(' '):
            continue
        d_tmp[sn]['sale_num']=sale_nums[idx]
        d_tmp[sn]['series_id'] = series_name_id[sn]

    for k,v in d_tmp.items():
        try:
            series_id = v['series_id']
            series_koubei = requests.get(host_koubei.format(series_id)).json()
            gkv = GetKeyValue(series_koubei,mode='j')
            advantage = ','.join(gkv.search_key('advantage')[0])
            shortcoming = ','.join(gkv.search_key('shortcoming')[0])
            price = gkv.search_key('price')
            username = gkv.search_key('username')
            specName = gkv.search_key('specName')
            v['user_name'] = username[0]
            v['advantages'] = advantage.replace(',',"，")
            v['shortcoming'] = shortcoming.replace(',',"，")
            v['price'] = price[0]
            v['spec_name'] = specName[0]
        except Exception as e:
            v['shortcoming'] = '暂无用户评论'
            v['advantages'] = '暂无用户评论'
            print(k,v)
            print(e)
            continue
    
    return d_tmp

def create_json(csv_dir='./sales_board_data'):
    csv_files = os.listdir(csv_dir)
    csv_files = [os.path.join(csv_dir,file) for file in csv_files if (file.endswith('csv') and not file.startswith('cumsum'))]
    df = DataFrame()
    for csv_file in csv_files:
        tmp = pd.read_csv(csv_file)
        df =  pd.concat([df,tmp],ignore_index=False)
    series_name_id = dict(zip(df['seriesname'].tolist(),df['seriesid'].tolist()))
    series_id_Name = dict(zip(df['seriesid'].tolist(),df['seriesname'].tolist()))
    with open('series_name_id.json','w') as f:
        f.write(json.dumps(series_name_id,ensure_ascii=False,indent=4))
    with open('series_id_name.json','w') as f:
        f.write(json.dumps(series_id_Name,ensure_ascii=False,indent=4))
    
    return series_name_id,series_id_Name
    
def get_brand():
    csv_file = 'brand_series_spec.csv'
    res_d = {}
    with open(csv_file,'r',encoding='utf-8') as f:
        for line in f:
            secs  = line.strip().split('\t')
            brand = secs[0]
            series = secs[1]
            res_d[series] = brand
    with open('series_brand.json','w') as f:
        f.write(json.dumps(res_d,ensure_ascii=False,indent=4))
    return 
    
