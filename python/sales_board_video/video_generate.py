import bar_chart_race as bcr
import pandas as pd
from pandas import DataFrame
import os
import moviepy.editor as mp
import cv2
import matplotlib.pyplot as plt

from collections import defaultdict
import numpy as np

from utils import *

import argparse


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def summary(res_df:dict, rank:int):
    max_sales = int(max(round(res_df)))
    id_max_sales = res_df.idxmax()
    s = f'No.1:{id_max_sales} {max_sales}'
    return {'x': .99, 'y': .05, 's': s, 'ha': 'right', 'size': 8}


def run(csv_dir,dimension,compare_list,series_name_id,video_title):
    '''
        dimension: 对比维度
        compare_list: 对比的内容(不同车系,不同等级等)
        csv_dir: 存储csv的路径,后缀要用日期表示(必须)
        video_title: 视频标题
    '''
    csv_files = os.listdir(csv_dir)
    csv_files = [os.path.join(csv_dir,file) for file in csv_files if file.endswith('csv')]
    res = defaultdict(dict)
    '''
    res: example:{'蔚来':{'2021-10':1000,'2021-11':2000,...},'理想':{'2021-10':1000,'2021-11':2000,...}...}
    '''
    for csv_file in csv_files:
        date = csv_file.rsplit('_',1)[-1].split('.')[0]
        df = pd.read_csv(csv_file)
        d_tmp = dict(zip(df[dimension].tolist(),df['a.clh_sale_num'].tolist()))
        for d in compare_list:
            try:
                res[d][date] = d_tmp[d]
            except Exception as e:
                res[d][date] = 0
    res_df = DataFrame(res)
    
    res_df_sum = res_df
    for d in compare_list:
        res_df_sum[d] = res_df[d].cumsum()
    res_df_sum_new = insert_pd(res_df_sum,fre=1)

    steps_per_period = 20
    bcr.bar_chart_race(res_df_sum_new,'res_wo_png.mp4',steps_per_period=steps_per_period,orientation='h',
            label_bars = True,
            title=video_title,
            period_summary_func=summary,
            period_length=steps_per_period*len(res_df)*5)

    video_duration = get_video_duration('res_wo_png.mp4')
    max_idx = res_df_sum_new.idxmax(axis=1).tolist()
    video_rows = len(max_idx)
    png_duration = []
    left,right = 0,0
    while right<len(max_idx):
        if max_idx[right]==max_idx[left]:
            right+=1
        else:
            png_duration.append([max_idx[left],(left,right)])
            get_png(series_id=series_name_id[max_idx[left]],series_name=max_idx[left])
            left = right
    png_duration.append([max_idx[left],(left,right)])
    get_png(series_id=series_name_id[max_idx[left]],series_name=max_idx[left])
    trans(png_duration,video_rows,video_duration)

    pic_num = 1
    ffmpeg_prefix = 'ffmpeg -y -i res_wo_png.mp4'
    scale_prefix = '[0:0]scale=iw:ih[a];'
    filter_prefix = ''
    for idx,png in enumerate(png_duration):
        pic_num+=1
        ffmpeg_prefix+=' -i {}.png'.format(png[0])
        if idx==0:
            scale_prefix+='[1:0]scale=300:-1[wm_{}];'.format(idx+1)
            filter_prefix+="[a][wm_{}]overlay=y=200:x=650:enable='between(t,{},{})'[v2];".format(idx+1,png[1][0],png[1][1])
        else:
            scale_prefix+='[{}:0]scale=300:-1[wm_{}];'.format(idx+1,idx+1)
            filter_prefix+="[v{}][wm_{}]overlay=y=200:x=650:enable='between(t, {},{})'[v{}];".format(idx+1,idx+1,png[1][0],png[1][1],idx+2)
    ffmpeg_cmd = ffmpeg_prefix+" -filter_complex "+'"{}{}"'.format(scale_prefix,filter_prefix.strip(';'))+" -map [v{}]".format(pic_num)+" -c:v libx264 result.mp4"
    os.system(ffmpeg_cmd)
    os.system('rm res_wo_png.mp4')


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--sales_data_dir',type=str,default='./sales_board_data')
    parser.add_argument('--dimension',type=str,default='a.series_name')
    # https://blog.csdn.net/kinggang2017/article/details/94036386
    parser.add_argument('--compare_list',nargs='+',type=str,help='<Required> compared car series',required=True)
    parser.add_argument('--video_title',type=str,required=True)
    args = parser.parse_args()

    if not os.path.isfile('series_name_id.json') or not os.path.isfile('series_id_name.json'):
        series_name_id,series_id_name=create_json(csv_dir='./sales_board_data')
    else:
        series_name_id = json.loads(open('series_name_id.json','r').read())
        series_id_name = json.loads(open('series_id_name.json','r').read())

    run(csv_dir=args.sales_data_dir,
        dimension=args.dimension,
        compare_list=args.compare_list,
        series_name_id=series_name_id,
        video_title=args.video_title)

    #compare_list=['蔚来ES6','蔚来ES8','理想ONE','小鹏P7','小鹏G3','小鹏P5','蔚来EC6','威马E.5','威马EX5','威马W6','威马EX5'],
#

