import requests
import json
import base64
import uuid
from PIL import Image
from io import BytesIO, StringIO
import numpy as np
from src.tools import *

public_key = 'templatebanner'
private_key = 'EfM&5pG*^h'
authorization = base64.b64encode(bytes(public_key + ':' + private_key, encoding='utf-8')).decode('utf-8')
headers_engine = {'Authorization': 'Basic ' + authorization}
public_key = 'aidesign-headmap'
private_key = 'u1OC8Gr7Iw'
authorization = base64.b64encode(bytes(public_key + ':' + private_key, encoding='utf-8')).decode('utf-8')
headers_detect = {'Authorization': 'Basic ' + authorization}

def get_component_boxes(picpath):
    with open(picpath, 'rb') as f:
        im_base64 = base64.b64encode(f.read()).decode('utf-8')

    host = "http://color.service.diana.corpautohome.com/detector/carparts"
    data = {}
    data['pvid'] = str(uuid.uuid4())
    data['image_base64'] = im_base64

    result = requests.post(host, json=data)
    json_res = json.loads(result.content)
    
    if json_res['returncode']!=0:
        return {}

    return json_res['result']

def get_car_boxes(picpath):
    im = Image.fromarray(picpath)
    #im = Image.open(picpath, 'r').convert('RGB')

    curw, curh = im.size
    if curw>1920 or curh>1080:
        neww, newh = resize_pic(curw, curh, 1920, 1080)
        #im = im.resize((neww, newh))

    byte_io = BytesIO()
    im.save(byte_io, 'JPEG')
    im_data = base64.b64encode(byte_io.getvalue())
    host = 'http://dmcv-common.openapi.corpautohome.com/detector/yolo'
    data = {}
    data['image_base64'] = im_data.decode()
    w, h = im.size
    result = requests.post(host, json=data, timeout=4, headers=headers_detect)
    result = eval(result.text)
    if result['returncode']!=0:
        box = []
    else:
        cars = result['cars']
        box = []
        for elements in [cars]:
            for element in elements:
                pos = element['position']
                lt, tp, rt, bt = pos[0], pos[1], pos[2], pos[3]
                box.append([lt,tp,rt,bt])

        leng = len(box)
        i = 0
        flag = 0
        for t in range(0, leng):
            tmp = box[t]
            if tmp[2]-tmp[0] > flag:
                i = t
                flag = tmp[2]-tmp[0]

    res = []
    if box!=[]:
        res = [box[i][0]*w, box[i][1]*h, box[i][2]*w, box[i][3]*h]
    return res
