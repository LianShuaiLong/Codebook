# encoding='utf-8'
import redis
import json
import argparse
import pandas as pd
from redis_utils.redis_op import *
from pprint import pprint
from datetime import datetime,timedelta
import os

def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_csv',type=str,default='./data/sales_board_2023-01.csv')
    parser.add_argument('--d_csv',action='store_true')
    parser.add_argument('--config_file',type=str,default='config.json')
    args = parser.parse_args()
    return args


def task_func(input_data):
    data_cmd = input_data['data_cmd']
    date_hor_30 = datetime.now() - timedelta(days=30)
    date_hor_30 = datetime.strftime(date_hor_30, '%Y-%m')
    if 'src_csv' in input_data:
        df = pd.read_csv(input_data['src_csv'])
    else:
        os.system(data_cmd)
        df = pd.read_csv(f'./data/sales_board_{date_hor_30}.csv')
    redis_config = input_data['redis_config']
    video_themes = input_data['video_themes']
    '''
    [
        汽车,
        ...
        大众,
        宝马,
        ...
    ]
    '''
    for video_theme in video_themes:
        if isinstance(video_theme,dict):
            continue
        else:
            if video_theme in set(df['car_type'].values):
                seriesName = list(df[df['car_type']==video_theme]['seriesname'])[:10]
                sales = list(df[df['car_type']==video_theme]['salecnt'])[:10]
            elif video_theme in set(df['spec_brand'].values):
                seriesName = list(df[df['spec_brand']==video_theme]['seriesname'])[:10]
                sales = list(df[df['spec_brand']==video_theme]['salecnt'])[:10]
            elif video_theme in set(df['spec_level'].values):
                seriesName = list(df[df['spec_level']==video_theme]['seriesname'])[:10]
                sales = list(df[df['spec_level']==video_theme]['salecnt'])[:10]
            elif video_theme in set(df['country'].values):
                seriesName = list(df[df['country']==video_theme]['seriesname'])[:10]
                sales = list(df[df['country']==video_theme]['salecnt'])[:10]
            elif video_theme == '新能源':
                seriesName = list(df[df['energy']==1]['seriesname'])[:10]
                sales = list(df[df['energy']==1]['salecnt'])[:10] 
            else:
                continue
        k_v = dict(zip(seriesName,sales))
        print(video_theme)
        pprint(k_v)
        write_redis(k_v,redis_config,name=video_theme)


if __name__=='__main__':
    
    args = parse_parser()
    config_file = args.config_file
    cfg = json.loads(open(config_file,'r').read())
    if not args.d_csv:
        src_csv = args.src_csv
        cfg['src_csv'] = src_csv
    task_func(cfg)

