#******************提取ImageNet预训练模型某层的feature map*********************#
import torch
import torch.nn as nn
import torchvision
from collections import OrderedDict
# vgg-16 relu5-3 feature
model = torchvision.models.vgg16(pretrained=True).features[:-1]
# vgg-16 pool5 feature
model = torchvision.models.vgg16(pretrained=True).features
# vgg-16 fc7 feature
model = torchvision.models.vgg16(pretrained=True)
model.classifier = nn.Sequential(*list(model.classifier.children())[-3])
# resnet GAP feature
model = torchvision.models.resnet18(pretrained=True)
model = nn.Sequential(OrderedDict(list(model.named_children())[:-1]))

with torch.no_grad():
    model.eval()
    embedding = model(image)

#**************************提取预训练模型多层特征*********************************#
class FeatureExtractor(nn.Module):
     """Helper class to extract several convolution features from the given
    pre-trained model.

    Attributes:
        _model, torch.nn.Module.
        _layers_to_extract, list<str> or set<str>

    Example:注意这里的使用方法
        >>> model = torchvision.models.resnet152(pretrained=True)
        >>> model = torch.nn.Sequential(collections.OrderedDict(
                list(model.named_children())[:-1]))
        >>> conv_representation = FeatureExtractor(
                pretrained_model=model,
                layers_to_extract={'layer1', 'layer2', 'layer3', 'layer4'})(image)
    """
    def __init__(self,pretrained_model,layers_to_extract):
        super(FeatureExtractor,self).__init__()
        self._model = pretrained_model
        self._model.eval()
        self._layers_to_extract = set(layers_to_extract)
    def forward(self,x):
        with torch.no_grad():
            embeddings = []
            for name,layer in self._model.named_children():
                x = layer(x)
                if name in self._layers_to_extract:
                    embeddings.append(x)
            return x

#*********************微调全连接层*****************************************#
model = torchvision.models.resnet18(pretrained=True)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(512,100)
optimizer = torch.optim.SGD(model.fc.parameters(),lr=1e-2,momentum=0.9,weight_decay=1e-4)

#********************以较大学习率调全连接层，较小学习率调卷积层*************#
model = torchvision.models.resnet18(pretrained=True)
finetuned_parameters = list(map(id,model.fc.parameters()))  # id函数返回对象的地址
# map() 会根据提供的函数对指定序列做映射
# 第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。
# map(function,iterable)
conv_parameters = (p for p in model.parameters() if id(p) not in finetuned_parameters)
parameters = [{'params':conv_parameters,'lr':1e-3},{'params':model.fc.parameters()}]
optimizer = torch.optim.SGD(parameters,lr=1e-2,momentum=0.9,weight_decay=1e-4)


# 得到视频数据的基本信息
import cv2
video = cv2.VideoCapture(video_path)
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(video.get(cv2.CAP_PROP_FPS))
video.release()

# TSN每段(segment)采样一帧视频
K = self._num_segments
if is_train:
    if num_frames > K:
        # Random index for each segment.
        frame_indices = torch.randint(
            high=num_frames // K, size=(K,), dtype=torch.long)
        frame_indices += num_frames // K * torch.arange(K)
    else:
        frame_indices = torch.randint(
            high=num_frames, size=(K - num_frames,), dtype=torch.long)
        frame_indices = torch.sort(torch.cat((
            torch.arange(num_frames), frame_indices)))[0]
else:
    if num_frames > K:
        # Middle index for each segment.
        frame_indices = num_frames / K // 2
        frame_indices += num_frames // K * torch.arange(K)
    else:
        frame_indices = torch.sort(torch.cat((                              
            torch.arange(num_frames), torch.arange(K - num_frames))))[0]
assert frame_indices.size() == (K,)
return [frame_indices[i] for i in range(K)]

# 训练过程中常用的数据处理方式
# 其中transforms.ToTensor()会将PIL格式的图像或者(H,W,C)格式且数值范围为[0,255]
# 的np.ndarray数组转为(C,H,W)格式并且数值范围在[0,1.0]范围内的tensor
transform = torchvision.transforms.Compose([
    torchvision.transforms.RandomResizedCrop(size=224,scale=(0.08, 1.0)),
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=(0.485, 0.456, 0.406),
                                     std=(0.229, 0.224, 0.225)),
])