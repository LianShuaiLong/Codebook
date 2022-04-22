import os

import torch
import torch.distributed as dist
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.nn.parallel import DistributedDataParallel as DDP
from timm.utils import AverageMeter

BATCH_SIZE = 256
EPOCHS = 5

# sync_bn_module = torch.nn.SyncBatchNorm.convert_sync_batchnorm(module, process_group)
# https://pytorch.org/docs/stable/generated/torch.nn.SyncBatchNorm.html?highlight=nn%20syncbatchnorm%20convert_sync_batchnorm#torch.nn.SyncBatchNorm.convert_sync_batchnorm
# 

if __name__ == "__main__":

    # 0. set up distributed device
    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"]) #还有一种方式是通过parse的方式传进来:torch.distributed.py
    # set your device to local rank using
    torch.cuda.set_device(local_rank)# before your code runs
    # In your training program, you are supposed to call the following function at the beginning to start the distributed backend. It is strongly recommended that init_method=env://
    dist.init_process_group(backend="nccl")
    # 将tensor或者模型分配到相应的设备上
    device = torch.device("cuda", local_rank)
    # torch.distributed.barrier()
    # torch.distributed.barrier 是用于不同进程间的同步，其原理很简单，就是每个进程进入这个函数后都会被阻塞，当所有进程都进入这个函数后，阻塞解除，继续向下执行
    # https://murphypei.github.io/blog/2021/05/torch-barrier-trap (尽量只在当前位置使用)

    print(f"[init] == local rank: {local_rank}, global rank: {rank} ==")

    # 1. define network
    net = torchvision.models.resnet18(pretrained=False, num_classes=10)
    net = net.to(device)
    # DistributedDataParallel
    # https://pytorch.org/docs/stable/distributed.html
    net = DDP(net, device_ids=[local_rank], output_device=local_rank)

    # 2. define dataloader
    trainset = torchvision.datasets.CIFAR10(
        root="./data",
        train=True,
        download=True,
        transform=transforms.Compose(
            [
                transforms.RandomCrop(32, padding=4),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(
                    (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
                ),
            ]
        ),
    )
    # DistributedSampler
    # torch.utils.data.distributed.DistributedSampler(dataset, num_replicas=None, rank=None, shuffle=True, seed=0, drop_last=False)
    # num_replicas (int, optional) – Number of processes participating in distributed training. By default, world_size is retrieved from the current distributed group
    # rank (int, optional) – Rank of the current process within num_replicas. By default, rank is retrieved from the current distributed group.
    train_sampler = torch.utils.data.distributed.DistributedSampler(
        trainset,
        shuffle=True,
    )
    train_loader = torch.utils.data.DataLoader(
        trainset,
        batch_size=BATCH_SIZE,
        num_workers=4,
        pin_memory=True,
        sampler=train_sampler,
    )

    # 3. define loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(
        net.parameters(),
        lr=0.01 * 2,
        momentum=0.9,
        weight_decay=0.0001,
        nesterov=True,
    )

    if rank == 0:
        print("            =======  Training  ======= \n")

    # 4. start to train
    net.train()
    for ep in range(1, EPOCHS + 1):
        # set sampler
        train_loader.sampler.set_epoch(ep)
        # In distributed mode, calling the set_epoch() method at the beginning of each epoch before creating the DataLoader iterator is necessary to make shuffling work properly across multiple epochs. Otherwise, the same ordering will be always used.
       
        loss_meter = AverageMeter()
        acc_meter = AverageMeter()

        for idx, (inputs, targets) in enumerate(train_loader):
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = net(inputs)

            loss = criterion(outputs, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            correct_cur = torch.eq(outputs.argmax(dim=1), targets).sum().item()

            loss_meter.update(loss.item(),targets.size(0))
            acc_meter.update(correct_cur/targets.size(0),targets.size(0)) 
            

            if  ((idx + 1) % 25 == 0 or (idx + 1) == len(train_loader)):
                print(f'===global_rank:{rank}|local_rank:{local_rank}|loss_avg:{loss_meter.avg:.4f}|acc_avg:{acc_meter.avg:.4f}===')
    if rank == 0:
        print("\n            =======  Training Finished  ======= \n")


# 用mp.spawn方式启动分布式的tutorial
# https://yangkky.github.io/2019/07/08/distributed-pytorch-tutorial.html