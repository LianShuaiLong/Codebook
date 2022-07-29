import onnxruntime
import cv2
import numpy as np
import pdb
image = cv2.imread('test4.jpg')
height,width = image.shape[:2]# H,W,C

# pre process
# pad to achieve image with square shape for avoding face deformation after resizing
if height>width:
    w_pad = int((height-width)/2)
    image = np.pad(image,((0,0),(w_pad,w_pad),(0,0)),mode='constant',constant_values=((255,255),(255,255),(255,255)))
else:
    h_pad = int((width-height)/2)
    image = np.pad(image,((h_pad,h_pad),(0,0),(0,0)),mode='constant',constant_values=((255,255),(255,255),(255,255)))
    

image = cv2.resize(image,(512,512)) # 与导出的onnx的input保持一致
image = image/np.max(image)
tmpImg = np.zeros((512,512,3))
tmpImg[:,:,0] = (image[:,:,2]-0.406)/0.225
tmpImg[:,:,1] = (image[:,:,1]-0.456)/0.224
tmpImg[:,:,2] = (image[:,:,0]-0.485)/0.229

tmpImg = tmpImg.transpose((2, 0, 1)).astype(np.float32)# HWC->CHW
tmpImg = tmpImg[np.newaxis,:,:,:]# CHW->NCHW

# inference
providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
onnx_session = onnxruntime.InferenceSession('u2net.onnx',providers=providers)
onnx_input = {'input':tmpImg}
onnx_output = onnx_session.run(['output0','output1','output2','output3','output4','output5','output6'],onnx_input)[0]


# post process
onnx_output = 1.0 - onnx_output[:,0,:,:]

onnx_output_max = np.max(onnx_output)
onnx_output_min = np.min(onnx_output)
onnx_output = (onnx_output-onnx_output_min)/(onnx_output_max-onnx_output_min)

onnx_output = np.squeeze(onnx_output,0)*255
onnx_output = np.clip(onnx_output,0,255)

cv2.imwrite('test4_onnx.jpg',onnx_output)
