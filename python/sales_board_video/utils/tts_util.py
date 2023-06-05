import requests
import json
import os

def tts_fn(txt, voice_choice=6):
    host = ""
    data = json.dumps({"text": txt})

    payload = {'mode': 1, 'voice': voice_choice,'speed':10}
    headers = \
        {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": ''
        }
    r = requests.post(host, data=data, headers=headers, params=payload,timeout=15)
    return r.content

# 设置前置静音1.5s,后置8.0-cover_time-1.5
def time_align(wav_len,wav_name,wav_expect_len,mute_time_before=0.01):
    wav_input = f'{wav_name}.wav'
    cover_total_time = wav_expect_len
    cover_mute_time_before = mute_time_before
    cover_mute_time_after = cover_total_time -cover_mute_time_before-wav_len
    cover_mute_name = "{}_mute.wav".format(wav_name)
    cmd = "ffmpeg -hide_banner -loglevel error -y -f lavfi -t {} -i anullsrc=channel_layout=stereo:sample_rate=22050 -i {} " \
        "-f lavfi -t {} -i anullsrc=channel_layout=stereo:sample_rate=22050 " \
        " -filter_complex \"[0:0] [1:0] concat=n=3:v=0:a=1 [a]\" -map [a] {}".format(
        cover_mute_time_before,
        wav_input,
        cover_mute_time_after,
        cover_mute_name)
    os.system(cmd)

