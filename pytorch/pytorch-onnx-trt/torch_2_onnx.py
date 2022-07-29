import torch
import torch.nn
import cv2
import time 

from model import U2NET

model_path='model/u2net_portrait.pth'
model = U2NET(3,1)
model.load_state_dict(torch.load(model_path))
input_tensor = torch.ones((1,3,512,512))

with torch.no_grad():
    torch.onnx.export(model,
            input_tensor,
            'u2net.onnx',
            opset_version=11,
            input_names=['input'],
            output_names=['output0','output1','output2','output3','output4','output5','output6'])

print('onnx model saved successfully...')
print('sleep 10s...')
time.sleep(10)
print('begin check onnx model...')

import onnx
onnx_model = onnx.load('u2net.onnx')
try:
    onnx.checker.check_model(onnx_model)
except Exception as e:
    print('model incorrect')
    print(e)
else:
    print('model correct')

