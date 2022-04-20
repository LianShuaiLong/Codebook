#**********************查看版本*********************#
import torch
import torch.nn as nn 
import torchvision
print(torch.__version__)
print(torch.backends.cuda)#查看cuda版本
print(torch.backends.cudnn.version())#查看cudnn版本
print(torch.cuda.get_device_name(0))#查看所使用的gpu

#*******************代码可复现性********************#
# 设置随机种子(在同一设备上保证可复现性)
# 程序开始的时候,固定torch的随机种子 固定numpy的随机种子
import numpy as np 
np.random.seed(0)
torch.manual_seed(0)
torch.cuda.manual_seed_all(0)

torch.backends.cudnn.deterministic = True #每次调用CuDNN采用确定的卷积操作，会导致网络变慢
torch.backends.cudnn.benchmark = False  #实现网络加速

#******************指定显卡**************************#
import os
os.environ['CUDA_VISIBLE_DEVICES']=''# CUDA_VISIBLE_DEVICES='' python *.py
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#************使用共用显卡时候,清除显存***************#
torch.cuda.empty_cache()
nvidia-smi --gpu-reset -i [gpu_id] 

