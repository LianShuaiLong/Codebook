# @v1 version:针对单个月的进行设计
import bar_chart_race as bcr
import pandas as pd
from pandas import DataFrame
import os
import moviepy.editor as mp
import cv2
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pdb
import argparse
import sys
sys.path.append('..')
from utils.common_util import *
from utils.t2_1 import *
from utils.tts_util import *
import random


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
voice_choice = 8#random.choice(['1','3','6','7'])


def run(csv_dir,csv_file,dimension,compare_list,series_name_id,video_title,tts_dir,vr_dir):
    # csv_files = os.listdir(csv_dir)
    # csv_files = [os.path.join(csv_dir,file) for file in csv_files if file.endswith('csv')]
    csv_file = csv_file
    res = defaultdict(dict)

    res_file_txt = open('filelist_slice.txt','w')
    video_prefix = 'video_slice'
    video_num= 0

    # for csv_file in csv_files:
    date = csv_file.rsplit('_',1)[-1].split('.')[0]
    df = pd.read_csv(csv_file)
    d_tmp = dict(zip(df[dimension].tolist(),df['salecnt'].tolist()))
    # 设置纵轴显示为' '*idx
    for idx,item in enumerate(compare_list):# 输入1->10排序的车系,显示时候10->1
        k = ' '*(idx+1)
        res[k][date]=0
    for idx,d in enumerate(compare_list[::-1]):
        try:
            res[d][date] = d_tmp[d]
            # 每新增一个车系,去除一个' '*idx
            k = " "*(idx+1)
            del res[k]
        except Exception as e:
            res[d][date] = 0
        
        # compare_list_tmp = compare_list[(len(compare_list)-1-idx):]
        res_df = DataFrame(res)
        # 输入1->10排序的车系,显示时候10->1
        res_df_sort = res_df.sort_values(by=date,axis=1,ascending=True)
        # res_df_sort_bak = res_df_sort.copy()
        steps_per_period = 20
        tmp_d = defaultdict(dict)
        # 设置0为初始值,然后插值,使得柱状图动起来
        for k,v in res.items():
            tmp_d[k]={date:0}
        
        tmp_list = compare_list[::-1]# 输入1->10排序的车系,显示时候10->1
        df_tmp = DataFrame(tmp_d)
        res_df = pd.concat([df_tmp,res_df_sort],ignore_index=False)
        res_df_sort = insert_pd(res_df,fre=20)
        # 新出一个车系的柱状图时，固定前序车系的柱状图
        if idx>=1:
            for j in range(0,idx):
                res_df_sort[tmp_list[idx-1-j]]=res_df_sort[tmp_list[idx-1-j]].values.tolist()[-1]

        bcr.bar_chart_race(res_df_sort,f'{video_prefix}_{idx}.mp4',steps_per_period=steps_per_period,orientation='h',
                label_bars = True,
                bar_size=.60,
                title=video_title,
                period_summary_func=None,
                period_length=steps_per_period*len(res_df),
                )
        video_num+=1
        # 修改分辨率
        os.system(f'ffmpeg -i {video_prefix}_{idx}.mp4 -vf scale=1280:720 {video_prefix}_{idx}_1280.mp4 -hide_banner')
        os.system(f'rm {video_prefix}_{idx}.mp4')
        # 修改fps
        os.system(f'ffmpeg -r 25 -i {video_prefix}_{idx}_1280.mp4 {video_prefix}_{idx}_25.mp4')
        os.system(f'rm {video_prefix}_{idx}_1280.mp4')
        # 添加图片:获取图片,添加特效
        get_png(series_id=series_name_id[d],series_name=d,vr_dir=vr_dir)
        ffmpeg_cmd = f'ffmpeg -y -i {video_prefix}_{idx}_25.mp4 -loop 1 -i {vr_dir}/{d.replace(" ","")}.png \
                    -filter_complex \
                    \"[1:0]fade=out:st=15.9:d=0.1,scale=-1:300[wm_1];\
                    [0:0][wm_1]overlay=y=175:x=850:shortest=1\" -c:v libx264 {video_prefix}_{idx}_png.mp4'
        os.system(ffmpeg_cmd)
        os.system(f'rm {video_prefix}_{idx}_25.mp4')
        # 添加口碑
        series_koubei = get_koubei(res_df_sort,series_name_id)[d]
        series_koubei_t = {}
        series_koubei_t['ranking'] = len(compare_list)-idx
        series_koubei_t['series'] = d
        series_koubei_t['sales'] = series_koubei['sale_num']
        series_koubei_t['advantage'] = series_koubei['advantages']
        series_koubei_t['shortcoming'] = series_koubei['shortcoming']
        # pdb.set_trace()
        cmd_tmp = subtitle_fadein_fadeout(video_path = f'{video_prefix}_{idx}_png.mp4',input=[series_koubei_t],start_free_time=0,interval_time=16)
        os.system(cmd_tmp)
        os.system(f'rm {video_prefix}_{idx}_png.mp4')
        os.system(f'mv 口碑.mp4 {video_prefix}_{idx}_koubei.mp4')
        # 获取tts
        car_series = d
        if idx==0 and series_koubei_t['advantage']!='暂无用户评论':
                tts_txt = f'{car_series}在销量排行榜中排名第{series_koubei_t["ranking"]},销量{series_koubei_t["sales"]}辆, \
                与销量榜第一有较大的差距,口碑用户评价,优点是{series_koubei_t["advantage"]},缺点是{series_koubei_t["shortcoming"]}'
        elif idx==len(compare_list)-1 and series_koubei_t['advantage']!='暂无用户评论':
            tts_txt = f'{car_series}在销量排行榜中勇夺第一,\
            销量{ series_koubei_t["sales"]}辆,口碑用户评价,优点是{series_koubei_t["advantage"]},缺点是{series_koubei_t["shortcoming"]}，以上就是汽车之家口碑用户对各车系的评价'
        elif series_koubei_t['advantage']=='暂无用户评论':
            tts_txt = f'{car_series}在销量排行榜中排名第{series_koubei_t["ranking"]},\
            销量{ series_koubei_t["sales"]}辆,该车暂无口碑用户评价，您可以前往汽车之家口碑频道与车友分享您的用车体验以及您认为的优点和缺点,我们也期待着您对{car_series}的真实评价'
        else:
            tts_txt = f'{car_series}在销量排行榜中排名第{series_koubei_t["ranking"]},\
            销量{ series_koubei_t["sales"]}辆,口碑用户评价,优点是{series_koubei_t["advantage"]},缺点是{series_koubei_t["shortcoming"]}'
        tts_res = tts_fn(txt=tts_txt,voice_choice=voice_choice)
        tts_length=float(len(tts_res))/44100
        with open(f'{tts_dir}/{car_series.replace(" ","")}.wav','wb') as f:
            f.write(tts_res)
        # tts对齐
        if car_series=='Model Y' or '途观L':
            wav_expect_len = 19
        else:
            wav_expect_len = 18
        if idx==len(compare_list)-1:
            wav_expect_len+=1
        time_align(wav_len=tts_length,wav_name=f'{tts_dir}/{car_series.replace(" ","")}',wav_expect_len=wav_expect_len,mute_time_before=0.01)
        # 合并tts和视频
        cmd = f'ffmpeg -hide_banner -loglevel error \
                -i {video_prefix}_{idx}_koubei.mp4 \
                -i {tts_dir}/{car_series.replace(" ","")}_mute.wav \
                -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 {video_prefix}_{idx}_final.mp4 -y'
        os.system(cmd)
        os.system(f'rm {video_prefix}_{idx}_koubei.mp4')

        res_file_txt.write(f'file {video_prefix}_{idx}_final.mp4'+'\n')
            
    res_file_txt.close()
    os.system('ffmpeg -f concat -safe 0 -i filelist_slice.txt -c copy -strict -2 final.mp4 -y')
    for i in range(video_num):
        os.system(f'rm {video_prefix}_{i}_final.mp4')
    # 添加片头
    os.system('ffmpeg -r 25 -loop 1 -i 001.png -pix_fmt yuv420p -vcodec libx264 -b:v 600k -r:v 25 -preset medium -crf 30 -s 1280x720 -vframes 250 -r 25 -t 4 封面.mp4 -y')
    # 封面添加文字
    # os.system('ffmpeg -i 封面.mp4 -vf drawtext="fontfile=MFZhuoHei-Regular.otf:fontcolor=white:fontsize=80:x=850:y=300:text="十月汽车"" -c:v libx264 -an -f mp4 封面_title.mp4 -y')
    cmd = 'ffmpeg -i 封面.mp4 -filter_complex "drawtext=fontfile=MFZhuoHei-Regular.otf:text="2022年11月":fontcolor=white:fontsize=80:x=750:y=200,drawtext=fontfile=MFZhuoHei-Regular.otf:text="15至20万汽车":x=800:y=350:fontsize=60:fontcolor=white" -c:v libx264 -an -f mp4 封面_title.mp4 -y'
    os.system(cmd)
    os.system('rm 封面.mp4')
    # 添加柱状特效
    ffmpeg_cmd = "ffmpeg -y -i 封面_title.mp4 -vf \"movie=007.png,scale=-1:118[mask0];\
                            movie=008.png,scale=-1:118[mask1];\
                            movie=009.png,scale=-1:118[mask2];\
                            movie=010.png,scale=-1:118[mask3];\
                            [vid0][mask0] overlay=x='if(lte(t,0.5),-618+(W-618)/0.5*t,0)':y=100[vid1];\
                            [vid1][mask1]overlay=x='if(between(t,0.5,1),-618+(W-618)/1.1*(t-0.5),-280)':y=225:enable='gte(t,0.5)'[vid2];\
                            [vid2][mask2] overlay=x='if(between(t,1,1.5),-618+(W-618)/0.5*(t-1),0)':y=350:enable='gte(t,1)'[vid3];\
                            [vid3][mask3] overlay=x='if(between(t,1.5,2),-618+(W-618)/2.3*(t-1.5),-450)':y=475:enable='gte(t,1.5)'[vid4]\" 封面_title_D.mp4 -y"
    os.system(ffmpeg_cmd)
    os.system('rm 封面_title.mp4')
    # 添加引导语
    intro = '11月份15万至20万汽车销量排行榜新鲜出炉'
    tts_res = tts_fn(txt=intro,voice_choice=voice_choice)
    tts_length=float(len(tts_res))/44100
    with open(f'{tts_dir}/intro.wav','wb') as f:
        f.write(tts_res)
    time_align(wav_len=tts_length,wav_name=f'{tts_dir}/intro',wav_expect_len=5,mute_time_before=0.01)
    cmd = f'ffmpeg -hide_banner -loglevel error \
                    -i 封面_title_D.mp4 \
                    -i {tts_dir}/intro_mute.wav \
                    -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 封面_final.mp4 -y'
    os.system(cmd)
    os.system('rm 封面_title_D.mp4')
    # 制作结尾
    os.system('ffmpeg -r 25 -loop 1 -i 结尾.png -pix_fmt yuv420p -vcodec libx264 -b:v 600k -r:v 25 -preset medium -crf 30 -s 1280x720 -vframes 250 -r 25 -t 3 结尾.mp4 -y')
    # 添加结束语
    intro = '也欢迎大家一起讨论'
    tts_res = tts_fn(txt=intro,voice_choice=voice_choice)
    tts_length=float(len(tts_res))/44100
    with open(f'{tts_dir}/ending.wav','wb') as f:
        f.write(tts_res)
    time_align(wav_len=tts_length,wav_name=f'{tts_dir}/ending',wav_expect_len=3,mute_time_before=0.01)
    cmd = f'ffmpeg -hide_banner -loglevel error \
                    -i 结尾.mp4 \
                    -i {tts_dir}/ending_mute.wav \
                    -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 结尾_final.mp4 -y'
    os.system(cmd)
    os.system('rm 结尾.mp4')
    
    # 中间部分添加背景图
    os.system('ffmpeg -i final.mp4 -vf scale=1024:576 final_1024.mp4 -hide_banner')
    os.system('rm final.mp4')
    os.system('ffmpeg -loop 1 -i 视频背景.png -i  final_1024.mp4 -filter_complex "overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p" -c:a copy final.mp4 -y')
    os.system('rm final_1024.mp4')
    # 合并视频
    with open('filelist_part.txt','w',encoding='utf-8') as f:
        f.write('file 封面_final.mp4'+'\n')
        f.write('file final.mp4'+'\n')
        f.write('file 结尾_final.mp4'+'\n')   
    os.system(f'ffmpeg -f concat -safe 0 -i filelist_part.txt -c copy -strict -2 {video_title}.mp4 -y')
    # 添加背景音乐
    video_duration = get_video_duration(f'{video_title}.mp4')
    os.system('ffmpeg -i BGM.m4a -ss 00:00:00.0 -t {} -acodec copy BGM_tmp.m4a'.format(video_duration))

    cmd = f"ffmpeg -hide_banner -loglevel error -y -i {video_title}.mp4 -stream_loop -1 -i  BGM_tmp.m4a -c:v copy -filter_complex \"[0:a]aformat=fltp:44100:stereo,volume=1.0[0a];" \
                  "[1]aformat=fltp:44100:stereo,apad,volume=0.11[1a];[1a]apad[a1];[0a][a1]amerge=inputs=2[a]\" -map 0:v -map \"[a]\" " \
                  " -ac 2 15至20万汽车.mp4"
    os.system(cmd)
    os.system(f'rm {video_title}.mp4')
    os.system('rm BGM_tmp.m4a')
    os.system('rm 封面_final.mp4')
    os.system('rm final.mp4')
    os.system('rm 结尾_final.mp4')
    

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--sales_data_dir',type=str,default='../sales_board_data')
    parser.add_argument('--csv_file',type=str,default='../sales_board_data/v2_data/sales_board_2022-11.csv')
    parser.add_argument('--dimension',type=str,default='seriesname')
    parser.add_argument('--compare_list',nargs='+',type=str,help='<Required> compared car series',required=True)
    parser.add_argument('--video_title',type=str,required=True)
    parser.add_argument('--vr_dir',type=str,default='../vr_imgs')
    parser.add_argument('--tts_dir',type=str,default='./tts_wavs')
    args = parser.parse_args()

    tts_dir = args.tts_dir
    vr_dir = args.vr_dir
    os.makedirs(tts_dir,exist_ok=True)
    os.makedirs(vr_dir,exist_ok=True)

    if not os.path.isfile('series_name_id.json') or not os.path.isfile('series_id_name.json'):
        series_name_id,series_id_name=create_json(csv_dir=args.sales_data_dir)
    else:
        series_name_id = json.loads(open('series_name_id.json','r').read())
        series_id_name = json.loads(open('series_id_name.json','r').read())

    run(csv_dir=args.sales_data_dir,
        csv_file = args.csv_file,
        dimension=args.dimension,
        compare_list=args.compare_list,
        series_name_id=series_name_id,
        video_title=args.video_title,
        tts_dir = tts_dir,
        vr_dir = vr_dir)
    
