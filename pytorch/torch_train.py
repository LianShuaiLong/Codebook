import torch
import torch.nn as nn 
import numpy as np


#********************模型训练*******************************#
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)
for epoch in range(train_epochs):
    for i,(images,labels) in enumerate(train_loader):
        images = images.cuda()
        labels = labels.cuda()
        outs = model(images)
        loss = criterion(outs,labels)

        # 根据pytorch中backward（）函数的计算，
        # 当网络参量进行反馈时，梯度是累积计算而不是被替换，
        # 但在处理每一个batch时并不需要与其他batch的梯度混合起来累积计算，
        # 因此需要对每个batch调用一遍zero_grad（）将参数梯度置0.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'Epoch:{epoch},Loss:{loss.item()}...')

#********************模型测试************************#
model.eval() #对于bn和drop_out 起作用

with torch.no_grad():
    correct = 0
    total = 0
    for images,labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        pred = torch.argmax(outputs,1).item()
        correct+= (torch.argmax(outputs,1)==labels).sum().cpu().data.numpy()
        total += len(images)
    print(f'acc:{correct/total:.3f}')


#****************自定义loss*************************#
class MyLoss(nn.Module):
    def __init__(self):
        super(MyLoss,self).__init__()
    def forward(self,x,y):
        looss = torch.mean((x-y)**2)
        return loss

#***************标签平滑,有很强的聚类效果？？？****************************#
# https://zhuanlan.zhihu.com/p/302843504 label smoothing 分析
# 写一个label_smoothing.py 的文件，然后再训练代码里面引用，用LSR代替交叉熵损失即可
import torch
import torch.nn as nn

class LSR(nn.Module):
    def __init__(self,e=0.1,reduction='mean'):
        super(LSR,self).__init__()
        self.log_softmax = nn.LogSoftmax(dim=1)
        self.e = e
        self.reduction = reduction
    
    def _one_hot(self,labels,classes,value=1):
        '''
            Convert labels to one hot vectors
        
        Args:
            labels: torch tensor in format [label1,label2,label3,...]
            classes: int,number of classes
            value: label value in one hot vector,default to 1

        Returns:
            return one hot format labels in shape [batchsize,classes]
        '''
        one_hot = torch.zeros(labels.size(0),classes)

        # labels and value_added size must match
        labels = labels.view(labels.size(0),-1)
        value_added = torch.Tensor(labels.size(0),1).fill_(value)
        value_added = value_added.to(labels.device)
        one_hot = one_hot.to(labels.device)

        one_hot.scatter_add_(1,labels,value_added) 
        # scatter_add_(dim, index_tensor, other_tensor) 
        # 将other_tensor中的数据，按照index_tensor中的索引位置，添加至one_hot中

    def _smooth_label(self,target,length,smooth_factor):
        '''
            Convert targets to one hot vector and smooth them
            eg:
                [1,0,0,0,0,0]->[0.9,0.02,0.02,0.02,0.02,0.02]
        
        Args:
            target: target in format[label1,label2,label3,...,label_batchsize]
            length: length of one-hot format(number of classes)
            smooth_factor: smooth factor for label smooth
        Returns:
            smoothed labels in one hot format
        '''
        one_hot = self._one_hot(target,length,value=1-smooth_factor)
        one_hot += smooth_factor/(length-1)
        
        return one_hot.to(target.device)

    def forward(self,x,target):# x,网络分类结果，shape=[B,num_classes]
        if x.size(0)!=target.size(0):
            raise ValueError(f'Expected input batchsize{x.size(0)} to match target batchsize {target.size(0)}')
        if x.dim()!=2:
            raise ValueError(f'Expected input tensor to have 2 dimensions,got {x.dim()}')
        smoothed_target = self._smooth_label(target,x.size(1),self.e)
        x = self.log_softmax(x)
        loss = torch.sum(-x*smoothed_target,dim=1)
        if self.reduction == 'None':
            return loss
        elif self.reduction == 'sum':
            return torch.sum(loss)
        elif self.reduction == 'mean':
            return torch.mean(loss)
        else:
            raise ValueError('Unrecongnized option,expect reduction to be one of none,mean,sum')
        
# 或者直接再训练过程中进行标签平滑

for images, labels in train_loader:
    images, labels = images.cuda(), labels.cuda()
    N = labels.size(0)
    # C is the number of classes.
    smoothed_labels = torch.full(size=(N, C), fill_value=0.1 / (C - 1)).cuda()
    smoothed_labels.scatter_(dim=1, index=torch.unsqueeze(labels, dim=1), value=0.9)

    score = model(images)
    log_prob = torch.nn.functional.log_softmax(score, dim=1)
    loss = -torch.sum(log_prob * smoothed_labels) / N
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
        

#******************************Mixup训练,数据增强的一种方式***********************************#
# mixup采用对不同类别之间进行建模的方式实现数据增强，而通用数据增强方法则是针对同一类做变换。(经验风险最小->邻域风险最小),提升对抗样本及噪声样本的鲁棒性
# 思路非常简单：
# 从训练样本中随机抽取两个样本进行简单的随机加权求和，同时样本的标签也对应加权求和，然后预测结果与加权求和之后的标签求损失，在反向求导更新参数。
# https://zhuanlan.zhihu.com/p/345224408
# distributions包含可参数化的概率分布和采样函数
beta_distribution = torch.distributions.beta.Beta(alpha, alpha)
for images, labels in train_loader:
    images, labels = images.cuda(), labels.cuda()

    # Mixup images and labels.
    lambda_ = beta_distribution.sample([]).item()
    index = torch.randperm(images.size(0)).cuda()
    mixed_images = lambda_ * images + (1 - lambda_) * images[index, :]
    label_a, label_b = labels, labels[index]

    # Mixup loss.
    scores = model(mixed_images)
    loss = (lambda_ * loss_function(scores, label_a)
            + (1 - lambda_) * loss_function(scores, label_b))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


#************************正则化***********************
# l1正则化
loss = nn.CrossEntropyLoss()
for param in model.parameters():
    loss += torch.sum(torch.abs(param))
loss.backward()

# l2正则化，pytorch中的weight_decay相当于l2正则化
bias_list = (param for name, param in model.named_parameters() if name[-4:] == 'bias')
others_list = (param for name, param in model.named_parameters() if name[-4:] != 'bias')
parameters = [{'parameters': bias_list, 'weight_decay': 0},                
              {'parameters': others_list}]
optimizer = torch.optim.SGD(parameters, lr=1e-2, momentum=0.9, weight_decay=1e-4)

#*********************梯度裁剪*************************#
torch.nn.utils.clip_grad_norm_(model.parameters(),max_norm=20)


#********************得到当前学习率*********************#

# If there is one global learning rate (which is the common case).
lr = next(iter(optimizer.param_groups))['lr']

# If there are multiple learning rates for different layers.
all_lr = []
for param_group in optimizer.param_groups:
    all_lr.append(param_group['lr'])

#在一个batch训练代码中,当前的lr是optimzer.param_groups[0]['lr']


#**********************学习率衰减************************#
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateaue(optimizer,mode='max',patience=5,verbose=True)

for epoch in range(num_epochs):
    train_one_epoch(...)
    val(...)
    scheduler.step(val_acc)

# Cosine annealing learning rate
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer=,T_max=80)
# Redule learning rate by 10 at given epochs
scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer,milestones=[50,70],gamma=0.1)
for t in range(0,80):
    scheduler.step()
    train(...)
    val(...)

# learning rate warmup by 10 epochs
# torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda, last_epoch=-1, verbose=False)
# 设置学习率为初始学习率乘以给定lr_lambda函数的值，lr_lambda一般输入为当前epoch
# https://blog.csdn.net/ltochange/article/details/116524264
scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer,lr_lambda=lambda t: t/10)
for t in range(0,10):
    scheduler.step()
    train(...)
    val(...)


#**********************优化器链式更新******************************#
# 从pytorch1.4版本开始，torch.optim.lr_scheduler支持链式更新(chaining)，即用户可以定义两个schedulers，并在训练过程中交替使用
import torch
from torch.optim import SGD
from torch.optim.lr_scheduler import ExponentialLR,StepLR
model = [torch.nn.Parameter(torch.randn(2,2,requires_grad=True))]
optimizer = SGD(model,0.1)
scheduler1 = ExponentialLR(optimizer,gamma=0.9)
scheduler2 = StepLR(optimizer,step_size=3,gamma=0.1)
for epoch in range(4):
    print(ecoch,scheduler2.get_last_lr()[0])
    print(epoch,scheduler1.get_last_lr()[0])
    optimizer.step()
    scheduler1.step()
    scheduler2.step()

#********************模型训练可视化*******************************#
# pytorch可以使用tensorboard来可视化训练过程
# pip install tensorboard
# tensorboard --logdir=runs
# 使用SummaryWriter类来收集和可视化相应的数据，为了方便查看，可以使用不同的文件夹，比如'loss/train'和'loss/test'

from torch.utils.tensorboard import SummaryWriter
import numpy as np

writer = SummaryWriter()

for n_iter in range(100):
    writer.add_scalar('loss/train',np.random.random(),n_iter)
    writer.add_scalar('loss/test',np.random.random(),n_iter)
    writer.add_scalar('Accuracy/train',np.random.random(),n_iter)
    writer.add_scalar('Accuracy/test',np.random.random(),n_iter)

#********************保存和加载检查点****************************#
start_epoch = 0
# Load checkpoint.
if resume: # resume为参数，第一次训练时设为0，中断再训练时设为1
    model_path = os.path.join('model', 'best_checkpoint.pth.tar')
    assert os.path.isfile(model_path)
    checkpoint = torch.load(model_path)
    best_acc = checkpoint['best_acc']
    start_epoch = checkpoint['epoch']
    model.load_state_dict(checkpoint['model'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    print('Load checkpoint at epoch {}.'.format(start_epoch))
    print('Best accuracy so far {}.'.format(best_acc))

# Train the model
for epoch in range(start_epoch, num_epochs): 
    ... 

    # Test the model
    ...

    # save checkpoint
    is_best = current_acc > best_acc
    best_acc = max(current_acc, best_acc)
    checkpoint = {
        'best_acc': best_acc,
        'epoch': epoch + 1,
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict(),
    }
    model_path = os.path.join('model', 'checkpoint.pth.tar')
    best_model_path = os.path.join('model', 'best_checkpoint.pth.tar')
    torch.save(checkpoint, model_path)
    if is_best:
        shutil.copy(model_path, best_model_path)
