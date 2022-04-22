# DDP distributed data parallel
# torch.distributed.launch
# 启动方式
# python -m torch.distributed.launch main.py 
'''

https://github.com/pytorch/examples/blob/main/distributed/ddp/README.md

N: number nodes
G: number GPUS per node
W: WorldSize,The total number of application processes running across all the nodes at one time
L: Local WorldSize,the number of processes running on each node
若每个GPU运行一个process,则L取值即为一个node上的GPU数量,W取值即为所有参与训练的GPU数量
Each application process is assigned two IDs: a local rank in [0, L-1] and a global rank in [0, W-1].
LOCAL_RANK取值[0,L-1],RANK取值[0,W-1]
Example: DDP 2nodes  4GPUs each nodes 每个进程占用2GPUS

NODE0:  
    train.py
    GLOABLE RANK:0
    LOCAL RANK:0
    GPU0 GPU1
    -----------------
    train.py
    GLOABLE RANK:1
    LOCAL RANK:1
    GPU2 GPU3
NODE1:  
    train.py
    GLOABLE RANK:2
    LOCAL RANK:0
    GPU0 GPU1
    -----------------
    train.py
    GLOABLE RANK:3
    LOCAL RANK:1
    GPU2 GPU3

a good rule of thumb is to have one process span a SINGLE GPU.(一个GPU上运行一个进程)

Independent of how a DDP application is launched, each process needs a mechanism to know its global and local ranks.
Once this is known, all processes create a ProcessGroup that enables them to participate in collective communication operations such as AllReduce.

通过launch.py启动DDP训练后,可以通过环境变量传递world size,global rank,master address 和master port 等参数,local_rank参数通过命令行参数的方式进行传递
所以在定义parser的时候,要parser.add_argument('--local_rank')
When the DDP application is started via launch.py, it passes the world size, global rank, master address and master port via environment variables 
and the local rank as a command-line parameter to each instance

The DDP application takes two command-line arguments:
--local_rank: This is passed in via launch.py更新之后从环境变量中读取,local_rank = int(os.environ['LOCAL_RANK'])
--local_world_size: This is passed in explicitly and is typically either $1$ or the number of GPUs per node.


'''
# DDP代码编写流程
'''
1.torch.distributed.init_process_group()初始化进程组
2.model = torch.nn.parallel.DistributedDataParallel(model)创建分布式模型
3.torch.utils.distributed.DistributedSampler(train_loader)创建DataLoader
4.调整其它必要的地方(tensor放到指定的device上,checkpoint保存,指标计算等)
5.使用torch.distributed.launch/torch.multiprocessing开始训练--对应不同的启动方式
'''

import argparse
import torch
import os
import torch.distributed as dist

def spmn_main(local_world_size,local_rank):
    # parameters used to initialize the process group
    env_dict = {key:os.environ[key] for key in ('MASTER_ADDR','MASTER_PORT','RANK','WORLD_SIZE')}
    print(f'[{os.get_pid()}] Initializing process group with:{env_dict}')
    # the process group is initialized with just the backend (NCCL or Gloo)
    # The rest of the information needed for rendezvous comes from environment variables set by launch.py(torch.distributed.launch)
    dist.init_process_group(backend='nccl')
    print(f'[{os,getpid()}] world_size ={dist.get_world_size()}'+f'rank={dist.get_rank()},backend={dist.get_backend()}')
    demo_basic(local_world_size,local_rank)
    dist.destroy_process_group()

def demo_basic(local_world_size,local_rank):
    # setup devices for this process
    # for local_world_size = 2,num_gpus=8
    # RANK 0 uses GPUS[0,1,2,3]
    # RANK 1 users GPUS[4,5,6,7]
    n = torch.cuda.device_count()//local_world_size #每个node所占的gpu数量
    device_ids = list(range(local_rank*n,(local_rank+1)*n))

    print(f'[{os.getpid()}] rank={dist.get_rank()},'+f'world_Size={dist.get_world_size()},n={n},device_ids={device_ids}')

    model =ToyModel().cuda(device_ids[0])
    ddp_model = torch.distributed.DistributedDataParallel(model,device_ids)

    loss = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(ddp_model.parameters(),lr=0.001)
    
    outputs = ddp_model(torch.randn(20,10))
    labels = torch.randn(20,5).to(device_ids[0])
    loss(outputs,labels).backward()
    optimizer.step()



if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_rank',type=int,default=0)
    parser.add_argument('--local_world_size',type=int,default=1)
    args = parser.parse_args()
    spmd_main(args.local_world_size,args.local_rank)

# on a 8 GPU node with one process per GPU:
# python -m torch.distributed.launch --nnode=1 --node_rank=0 --nproc_per_node=8 example.py --local_world_size=8
# be launched with a single process that spans all 8 GPUs
# python -m torch.distributed.launch --nnode=1 --node_rank=0 --nproc_per_node=1 example.py --local_world_size=1
# https://zhuanlan.zhihu.com/p/76638962
# --node_rank 多节点分布式训练时，指定当前节点的rank
# --nnodes 使用的节点数
# --nproc_per_node 指定当前节点上，使用GPU训练的进程数。建议将该参数设置为当前节点的 GPU 数量，这样每个进程都能单独控制一个 GPU,效率最高。

# torch.distributed 提供了一个启动工具，即 torch.distributed.launch，用于在***每个单节点***上启动多个分布式进程

# 单节点多进程分布式训练
# python -m torch.distributed.launch 
#       --nproc_per_node=NUM_GPUS_YOU_HAVE 
#       YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3 and all other arguments of your training script)

# 多节点多进程分布式训练
# Node1:
# python -m torch.distributed.launch 
#        --nproc_per_node=NUM_GPUS_YOU_HAVE 
#        --nnodes=2 
#        --node_rank=0 ------------
#        --master_addr="192.168.1.1" 
#        --master_port=1234 
#        YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3 and all other arguments of your training script)
# Node2:
# python -m torch.distributed.launch 
#       --nproc_per_node=NUM_GPUS_YOU_HAVE 
#       --nnodes=2 
#       --node_rank=1  ----------
#       --master_addr="192.168.1.1" 
#       --master_port=1234 
#       YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3 and all other arguments of your training script)

# 查看帮助
# python -m torch.distributed.launch --help