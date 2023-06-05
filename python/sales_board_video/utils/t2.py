# -*- coding:utf-8 -*-



import sys 
sys.path.append('../Fonts/')


def subtitle_fadein_fadeout(video_path, input, start_free_time, interval_time):
    # parmas input format [{}]
    cmd = "ffmpeg -y -i {} -filter_complex \"".format(video_path)
    if len(input) == 0:
        return None
    input_len = len(input)
    cmd += "[0]split={} ".format(input_len + 1)
    for i in range(input_len + 1):
        cmd += "[vid" + str(i) + "]"
    cmd += ";"
    cnt = 0
    fontfile = "MFZhuoHei-Regular.otf"
    for one_dt in input:
        series = one_dt['series']
        ranking = one_dt['ranking']
        sales = one_dt['sales']
        advantage = one_dt['advantage']
        shortcoming = one_dt['shortcoming']
        fade_in_time = start_free_time + cnt * interval_time
        fade_out_time = start_free_time + (cnt + 1) * interval_time
        cnt += 1
        cmd += "[vid{}]drawtext=fontfile={}:text=车系：{}:" \
               "fontcolor=black:fontsize=20:x=880:y=400,drawtext=fontfile={}:text=排行榜：{}:" \
               "fontcolor=red:fontsize=20:x=880:y=430,drawtext=fontfile={}:text=销量：{}:" \
               "fontcolor=red:fontsize=20:x=880:y=460,drawtext=fontfile={}:text=优点：{}:" \
               "fontcolor=black:fontsize=20:x=880:y=490,drawtext=fontfile={}:text=缺点：{}:" \
               "fontcolor=black:fontsize=20:x=880:y=520,fade=t=in:st={}:d=0.5:alpha=1,fade=t=out:st={}:d=0.5:alpha=1[v{}];".format(
            cnt, fontfile, series, fontfile, ranking, fontfile, sales, fontfile, advantage, fontfile,
            shortcoming, fade_in_time, fade_out_time, cnt)

    for i in range(input_len):
        if i == 0:
            cmd += "[vid0]"
            cmd += "[v" + str(i + 1) + "]overlay[video" + str(i) + "];"
        elif i > 0 and i < input_len - 1:
            cmd += "[video" + str(i - 1) + "][v" + str(i + 1) + "]overlay[video" + str(i) + "];"
        else:
            cmd += "[video" + str(i - 1) + "][v" + str(i + 1) + "]overlay"
    cmd += "\" 口碑.mp4"
    if input_len == 1:
        cmd = cmd.replace("[video0];", "")
    return cmd


def tts(txt, voice_choice):
    host = "http://tts.prod.service.diana.corpautohome.com/qicheren/synthesize"
    data = json.dumps({"text": txt})

    payload = {'mode': 1, 'voice': voice_choice}
    headers = \
        {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": ''
        }
    r = requests.post(host, data=data, headers=headers, params=payload)
    return r.content


if __name__ == '__main__':
    import os
    video_path = "口碑_png.mp4"
    input = [{"series": "威马W6", "ranking": "第一", "sales": "30000台", "advantage": "很好", "shortcoming": "不好"},
             {"series": "威马W7", "ranking": "第二", "sales": "20000台", "advantage": "很好啊", "shortcoming": "不好啊"},
             {"series": "威马W8", "ranking": "第三", "sales": "10000台", "advantage": "很好啊啊", "shortcoming": "不好啊啊"}]
    start_free_time = 1
    interval_time = 16
    cmd_shell = subtitle_fadein_fadeout(video_path, input, start_free_time, interval_time)
    os.system(cmd_shell)
    print(cmd_shell)
