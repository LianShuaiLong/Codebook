'''
                dtype                         9种CPU类型Tensor                9种GPU类型Tensor
    32位浮点型:torch.float32 or torch.float   torch.FloatTensor               torch.cuda.FloatTensor
    64位浮点型:torch.float64 or torch.double  torch.DoubleTensor              torch.cuda.DoubleTensor
    16位浮点型:torch.float16 or torch.half    torch.HalfTensor                torch.cuda.HalfTensor
    8位整型   :torch.unit8                    torch.ByteTensor                torch.cuda.ByteTensor
    8位整型   :torch.int8                     torch.CharTensor                torch.cuda.CharTensor
    16位整型  :torch.int16 or torch.short     torch.ShortTensor               torch.cuda.ShortTensor
    32位整型  :torch.int32 or torch.int       torch.IntTensor                 torch.cuda.IntTensor
    64位整型  :torch.int64 or torch.long      torch.LongTensor                torch.cuda.LongTensor
    布尔型    :torch.bool                     torch.BoolTensor                torch.cuda.BoolTensor         
    
    pytorch中Tensor的默认顺序:[N,C,H,W]
    并且数据范围[0,1]******************
    与PIL.Image进行转换的时候,需要转置和规范化        
'''
import torch
tensor = torch.randn(3,4,5)
print(torch.type())
print(torch.size())
print(torch.dim())

#**************张量命名,可以方便的使用维度的名称进行索引*****************#
# before 1.3 需要注释
# Tensor[N,C,H,W]
images = torch.randn(32,3,56,56)
images.sum(dim=1)
images.select(dim=1,index=0)

# after 1.3
NCHW = ['N','C','H','W']
images = torch.randn(32,3,56,56,names=NCHW)
images.sum('C')
images.select(dim=1,index=0)
#也可以这么设置
tensor = torch.randn(3,4,1,2,names=('C','N','H','W'))
#使用align_to可以对维度进行排序
tensor = tensor.align_to('N','C','H','W')#size[4,3,1,2]


#**************数据类型转换**************************#
#设置默认数据类型,pytorch种torch.FloatTensor要远快于torch.DoubleTensor
torch.set_deafault_tensor_type(torch.FloatTensor)

tensor = tensor.cuda()
tensor = tensor.cpu()
tensor = tesor.float()
tensor = tensor.long()

# torch.Tensor<-->np.ndarray
#除了CharTensor,所有*cpu上的tensor*都支持与numpy格式的相互转换
import numpy as np
ndarray = tensor.cpu().numpy()
tensor = torch.from_numpy(ndarray).float()
tensor = torch.from_numpy(ndarray.copy()).float()#If ndarray has negative stride.

# torch.Tensor<-->PIL.Image
# Tensor->PIL.Image
# [:,C,H,W]->[:,H,W,C]
import PIL
image = PIL.Image.fromarray(torch.clamp(tensor*255,min=0,max=255).byte().permute(1,2,0).cpu().numpy())
image = torchvision.transforms.functional.to_pil_image(tensor)
# PIL.Image->Tensor
# [:,H,W,C]->[:,C,H,W]
path = './test.jpg'
tensor = torch.from_numpy(np.asarray(PIL.Image.open(path))).permute(2,0,1).float()/255
tensor = torchvision.transforms.functional.to_tensor(PIL.Image.open(path))
# 或者直接采用transforms的形式transforms.ToTensor()

# np.ndarray<-->PIL.Image
image = PIL.Image.fromarray(np.ndarray.astype(np.unit8))
ndarray = np.asarray(PIL.Image.open(path))

# torch.Tensor---np.ndarray------PIL.Image


# 从只包含一个元素的张量中提取值
value = torch.rand(1).item()

# 张量变行(卷积层->全连接)
# 相比于torch.vire,torch.reshape可以自动处理输入张量不连续的情况
tensor = torch.randn(2,3,4)
shape = (6,4)
tensor = torch.reshape(tensor,shape)

# 打乱顺序
tensor = tensor[torch.randperm(tensor.size(0))] #打乱第一个维度
# 水平翻转[N,C,H,W]
# pytorch不支持tensor[::-1]这样的负步长操作
tensor = tensor[:,:,:,torch.arange(tensor.size()[3]-1,-1,-1).long()]
tensor = tensor[:,:,:,torch.arange(tensor.size(3)-1,-1,-1).long()]

# 复制张量
tensor.clone()         #生成新的tensor        原tensor依然在计算图中
tensor.detach()        #与原tensor共享内存    原tensor不在计算图中
tensor.detach().clone() #生成新的tensor       原tensor不在计算图中

# 张量拼接
# torch.cat是沿着指定维度进行拼接
# torch.stack会新增一维
# 当参数是3个10x5的张量，torch.cat的结果是一个30x5的tensor,而torch.stack的结果是[3,10,5]的tensor
tensor = torch.cat(list_of_tensors,dim=0)   #拼接
tensor = torch.stack(list_of_tensors,dim=0) #叠加

# 将整数label转为one-hot编码
tensor = torch.tensor([0,2,1,3]) #注意这个是利用list初始化了一个tensor,不是定义形状
N=tensor.size(0)
num_classes = 4
one_hot = torch.zeros(N,num_classes).long()
# [0,2,1,3]->[[0],[2],[1],[3]]
one_hot.scatter_(dim=1,index = torch.unsqueeze(tensor,dim=1),src=torch.ones(N,num_classes).long())

# 得到非零元素
torch.nonzero(tensor) # index of non-zero elements
torch.nonzero(tensor==0) # index of zero elements
torch.nonzero(tensor).size(0) #number of non-zero elements
torch.nonzero(tensor==0).size(0) #number of zero elements

# 判断两个张量相等
torch.allclose(tensor1,tensor2) # float tensor
torch.equal(tensor1,tensor2) # int tensor

# 张量扩展
tensor = torch.randn(64,512)
torch.reshape(tensor,(64,512,1,1)).expand(64,512,7,7)

#**************************矩阵乘法***************************#
# (m*n)*(n*p)->(m*p)
result = torch.mm(tensor1,tensor2)

#b*(m*n) * b*(n*p)->b*(m*p)
result = torch.bmm(tensor1,tensor2)

# element-wise multipulation
result = tensor1*tensor2

#********************计算两组数据的欧式距离*******************#
#利用broadcast机制
dist = torch.sqrt(torch.sum((X1[:,None,:]-X2)**2,dim=2))

#********************改变张量(维度)顺序****************************#
# 利用rearrange
'''
    1.将图像分成patch,并将patch进行向量化,合并成num_patches*(patch_size*image_channels)的二维矩阵
    2.将得到的二维矩阵还原成原来的图像
'''
from PIL import Image
from einops import rearrange
from torchvision import transforms

image_path = './test.jpg'
image_data = Image.open(image_path)
trans = transforms.Compose([transforms.CenterCrop((304,304)),transforms.ToTensor()])
img_tensor = trans(image_data)
img_pil = transforms.functional.to_pil_image(img_tensor)
img_pil.save('img_pil.jpg')
# p1:patch_size_h p2:patch_size_w h: num_patches in 'Height' w:num_patches in 'Width'
img_patches = rearrange(img_tensor,'c (h p1) (w p2)->(h w) (p1 p2 c)',p1=16,p2=16)

img_decoded = rearrange(img_patches,'(h w) (p1 p2 c)->c (h p1) (w p2)',h=19,w=19,p1=16,p2=16)
img_ded = transforms.functional.to_pil_image(img_decoded)
img_ded.save('img_decoded.jpg')

print('1:',img_patches.shape)
img_pat = transforms.functional.to_pil_image(img_patches)
# https://pytorch.org/vision/main/_modules/torchvision/transforms/functional.html#to_pil_image
# 源码实现的时候也是先将tensor转成ndarray(若tensor或者ndarray是二维的,会进行unsqueeze操作(CHW)或者expand_dims操作(HWC)
# 然后转成Image(Image.fromarray)
print('2:',img_patches.shape)
img_pat.save('img_patches.jpg')