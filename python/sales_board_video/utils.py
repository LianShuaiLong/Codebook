import pandas as pd
from pandas import DataFrame
import cv2
import json
import os

from collections import defaultdict
import numpy as np

import requests


host_vr = ''

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

def get_png(series_id,series_name):
    response = requests.get(host_vr.format(series_id))
    data = json.loads(response.content)
    vr_img = data['result']['color_list'][0]['Hori']['Normal'][0]['Url']
    with open(f'{series_name}.png','wb') as f:
        f.write(requests.get(vr_img).content)

def create_json(csv_dir='./sales_board_data'):
    csv_files = os.listdir(csv_dir)
    csv_files = [os.path.join(csv_dir,file) for file in csv_files if file.endswith('csv')]
    df = DataFrame()
    for csv_file in csv_files:
        tmp = pd.read_csv(csv_file)
        df =  pd.concat([df,tmp],ignore_index=False)
    series_name_id = dict(zip(df['a.series_name'].tolist(),df['a.series_id'].tolist()))
    series_id_Name = dict(zip(df['a.series_id'].tolist(),df['a.series_name'].tolist()))
    with open('series_name_id.json','w') as f:
        f.write(json.dumps(series_name_id,ensure_ascii=False,indent=4))
    with open('series_id_name.json','w') as f:
        f.write(json.dumps(series_id_Name,ensure_ascii=False,indent=4))
    
    return series_name_id,series_id_Name
    
