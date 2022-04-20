# copy from https://github.com/LianShuaiLong/CV_Applications/blob/master/classification/classification-pytorch/backbones/vgg19.py
import torch
import torch.nn as nn

class ConvNet(nn.Module):
    def __init__(self,in_channels,num_classes,bn=False):
        super(ConvNet,self).__init__()#调用父类的初始化函数
        self.num_classes = num_classes
        self.in_channels = in_channels
        self.bn = bn
        # simple model define
        # self.layer1 = nn.Sequential(
        #     nn.Conv2d(in_channels=in_channels,out_channels=64,kernel_size=3,stride=1,padding=2),
        #     nn.BatchNorm2d(num_features=64),
        #     nn.ReLU(inplace=True)
        #     nn.MaxPool2d(kernel_size=2,stride=1)
        # )
        # self.layer2 = nn.Sequential(
        #     nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3,stride=1,padding=1),
        #     nn.BatchNorm2d(num_features=128),
        #     nn.ReLU(),
        #     nn.MaxPool2d(kernel_size=2,stride=2)
        # )
        # self.fc = nn.Linear(in_features=7*7*128,out_features=num_classes)
        
        # network define
        out_channels = [3,64,128,256,512,512]
        repeat = [2,2,4,4,4]
        self.stage1 = self._make_stage(
            in_channels=out_channels[0],
            out_channels=out_channels[1],
            repeat=repeat[0]
        )
        self.max_pool1 = nn.MaxPool2d(kernel_size=2,stride=2)
        self.stage2 = self._make_stage(
            in_channels = out_channels[1],
            out_channels = out_channels[2],
            repeat=repeat[1]
        )
        self.max_pool2 = nn.MaxPool2d(kernel_size=2,stride=2)
        self.stage3 = self._make_stage(
            in_channels= out_channels[2],
            out_channels= out_channels[3],
            repeat = repeat[3]
        )
        self.max_pool3 = nn.MaxPool2d(kernel_size=2,stride=2)
        self.stage4 = self._make_stage(
            in_channels=out_channels[3],
            out_channels=out_channels[4]
            repeat = repeat[4]
        )
        self.max_pool4 = nn.MaxPool2d(kernel_size=2,stride=2)
        self.stage5 = self._make_stage(
            in_channels=out_channels[4],
            out_channels=out_channels[5],
            repeat=repeat[5]
        )
        self.max_pool5 = nn.MaxPool2d(kernel_size=2,stride=2)
        self.classifier = nn.Sequential(
            nn.Linear(512*7*7,4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096,4096),
            nn.ReLU(inplace=True),
            nn.Dropout()
            nn.Linear(4096,num_classes)
        )
        # module initialization
        for layer in self.modules():
            if isinstance(layer,nn.Conv2d):
                self._init_conv(layer)
            elif isinstance(layer,nn.InstanceNorm2d):
                self._init_norm(layer)
            elif isinstance(layer,nn.BatchNorm2d):
                self._init_norm(layer)
            elif isinstance(layer,nn.Linear):
                self._init_fc(layer)
        # show network
        self._show_network()

    def _make_stage(self,in_channels,out_channels,repeat):
        stage = []
        for i in range(repeat):
            # https://zhuanlan.zhihu.com/p/494661681
            # preNorm(先归一化然后conv) 的效果 比 postNorm(先conv后归一化)的迁移效果差
            # 与RELU无关
            # inplace = True表示原地修改,节省内存
            # https://www.cnblogs.com/wanghui-garcia/p/10642665.html
            stage.append(nn.Conv2d(in_channels,out_channels,kernel_size=3,stride=1,padding=1))
            stage.append(nn.ReLU(inplace=True))
            if self.bn:
                stage.append(nn.BatchNorm2d(num_features=out_channels))
        return nn.Sequential(*stage)
    
    def _show_network(self):
        # model.children()与model.modules()的区别：
        # model.children()只会遍历模型的下一层
        # model.modules()会迭代地遍历模型的所有子层
        for idx,m in enumerate(self.children()):
            print(idx,'--->',m)
    
    def _init_conv(self,conv):
        nn.init.kaiming_uniform_(conv.weight,a=0, mode='fan_in', nonlinearity='relu')
        if conv.bias is not None:
            nn.init.constant_(conv.bias,0)
    def _init_norm(self,norm):
        if norm.weight is not None:
            '''
            norm.weight:Gamma
            norm.bias:beta
            https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html?highlight=batchnorm#torch.nn.BatchNorm2d
            '''
            nn.init.constant_(norm.weight,1)
            nn.init.constant_(norm.bias,0)
    def _init_fc(self,fc):
        nn.init.normal_(fc.weight,0,0.01)
        nn.init.constant_(fc.bias,0)

    def forward_features(self,x):
        # x = self.layer1(x)
        # x = self.layer2(x)
        # x = x.reshape(x.size(0),-1)
        # return x
        x = self.stage1(x)
        x = self.max_pool1(x)
        x = self.stage2(x)
        x = self.max_pool2(x)
        x = self.stage3(x)
        x = self.max_pool3(x)
        x = self.stage4(x)
        x = self.max_pool4(x)
        x = self.stage5(x)
        x = self.max_pool5(x)
        x = torch.flatten(x,1)#torch.flatten(input,start_dim=0,end_dim=-1)
        return x
    def forward(self,x):
        x = self.forward_features(x)
        x = self.classifier(x)
        return x

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = ConvNet(in_channels=3,num_classes=1000,bn=True).to(device)


# 双线性汇合 biliear pooling  ？？？？？？？？？？？？？？存疑
x = torch.reshape(x,[N,D,H*W])
x = torch.bmm(x,torch.transpose(x,dim0=1,dim1=2))/(H*W)#x->[N,D,D]
x = torch.reshape(x,[N,D*D])
x = torch.sign(x)*torch.sqrt(abs(x)+1e-5)
x = torch.nn.functional.normalize(x)

# 多张卡同步BN
# 当使用torch.nn.DataParallel进行并行训练时候,每张卡上的BN统计值variance和mean是
# 独立计算的,同步BN使所有卡上的数据一起计算variance和mean有利于缓解当前batchsize
# 比较小导致的mean和variance不准的问题，是在目标检测等任务上提升的一个小技巧
sync_bn = torch.nn.SyncBatchNorm(num_features,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
# 将已有网络中的bn改为sync_bn
def convertBNtoSyncBN(module,process_group=None):
    '''
    Recursively replace BN layer with SyncBN layer
    
    Args:
        module : torch.nn.Module
    '''
    if isinstance(module,torch.nn.modules.batchnorm._BatchNorm):
        sync_bn = torch.nn.SyncBatchNorm(
            num_features=module.num_features,
            eps=module.eps,
            affine=module.affine,# gamma and beta
            track_running_stats= module.track_running_stats # default = True
            # If track_running_stats is set to False, 
            # this layer then does not keep running estimates, 
            # and batch statistics are instead used during evaluation time as well
            # This momentum argument is different from one used in optimizer classes and 
            # the conventional notion of momentum
            # Mathematically, the update rule for running statistics here is
            # x_new = (1-momentum)*x_estimate+momentum*x_now 
        )
        sync_bn.running_mean = module.running_mean
        sync_bn.running_var = module.running_var
        if sync_bn.affine:
            sync_bn.weight = module.weight.clone().detach()  
            sync_bn.bias = module.bias.clone().deteach()
        return sync_bn
    else:
        for name,child_module in module.named_children():
            setattr(module,name) = convert_syncbn_model(child_module,process_group=process_group)
        return module


# 类似BN滑动平均,需要在forward函数中采用inplace对操作进行复制
class BN(nn.Module):
    def __init__(self):
        super(BN,self).__init__()
        self.register_buffer('running_mean',tensor=torch.zeros(num_features))
    def forward(self,X):
        self.running_mean += momentum*(current - self.running_mean)
        # mean_new = (1-momentum)*mean_estimate+momentum*mean_now

# 计算模型参数量
# torch.numel:Returns the total number of elements in the input tensor.
model_parameters = sum(torch.numel(paramter) for paramter in model.parameters())

# 查看网络的参数
# 通过model.state_dict()或者model.named_parameters()查看现在全部可训练的参数
params = list(model.named_parameters())
name,param = params[1]
print(name)
print(param.grad)

# pytorch模型可视化
# https://github.com/szagoruyko/pytorchviz

# pytorch-summary() 与 keras中的model.summary()类似
# https://github.com/sksq96/pytorch-summary


# 提取模型的某一层
# model.modules()会返回模型中所有模块的迭代器，可以访问到最内层，例如self.layer1.conv1这个模块
# model.children()只能访问到模型的下一层，例如self.layer1这一层
# 与之对应的named_modules()和named_children()属性,不仅会返回迭代器，还会返回层的名称
# 取模型的前两层
new_model = nn.Sequential(*(list(model.children())[:2]))
# 取模型所有的卷积层
for layer in model.named_modules():
    if isinstance(layer[1],nn.Conv2d):
        conv_model.add_module(layer[0],layer[1])# name,module

# 部分层使用预训练的权重
# 注意如果保存的模型是nn.DataParallel,则这种情况下也需要先将model设置为nn.DataParallel
# model = nn.DataParallel(model).cuda()
# strict = False忽略OrderedDict(state_dict存储的格式)中不匹配的key
model.load_state_dict(torch.load(pretrain_model_path),strict=False)


# 将GPU保存的模型加载的cpu上,采用map_location
model.load_state_dict(torch.load(pretrain_model_path,map_location='cpu'))

