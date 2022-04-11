#https://www.pythonf.cn/read/158810
import pynvml
from pynvml import *
import os
import sys
import signal

MEMORY_THESHOLD=10
nvmlInit()
print ("Driver Version:", nvmlSystemGetDriverVersion())
deviceCount = nvmlDeviceGetCount()
GPU_AVILIABLE=[]
while 1:
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        memo_total = meminfo.total/(1024*1024*1024)
        memo_used = meminfo.used/(1024*1024*1024)
        if memo_total>=MEMORY_THESHOLD and memo_used/memo_total<=0.2:
            GPU_AVILIABLE.append(i)
        if len(GPU_AVILIABLE)==0:
            print('No GPU Is Avilable!')
        else:
            print('Avilable GPUS:',GPU_AVILIABLE)
            print(f'Start to train with GPU:{GPU_AVILIABLE}...')
            cmd =''
            os.system(cmd)
            #sys.exit(1)
			os.kill(os.getpid(),signal.SIGKILL)
