import json
import random

class multi_random_sample(object):
    '''
    不仅支持[1,2,3,4]这种形式的list(这种可以直接利用set进行操作)
    而且支持[{},{},{},(),()]这种形式的list
    '''
    def __init__(self,src:list,sample_list:list):
        super(multi_random_sample,self).__init__()
        self.src = src
        self.sample_list = sample_list
        sample_rate=[item/sum(sample_list) for item in sample_list]
        self.sample_nums=[round(len(src)*sample_rate[i]) for i in range(len(sample_list)-1)]
        self.sample_nums.append(len(src)-sum(self.sample_nums))
        self.samples_left = list(enumerate(src))
        self.sample_num_used=0
        self.samples_res= []
    def run(self):
        for sample_num in self.sample_nums:
            sample_slice=random.sample(self.samples_left[:(len(self.src)-self.sample_num_used)],sample_num)
            sample_idx = set([item[0] for item in sample_slice])
            self.samples_res.append([item[-1] for item in sample_slice])
            # initial version:用另外一个数组来存储剩余的sample
            # samples_left_new=[]
            # for idx,item in samples_left:
            #     if idx in sample_idx:
            #         continue
            #     else:
            #         samples_left_new.append((idx,item))
            # samples_left=samples_left_new
            # v1:采用原地修改的方法，不用申请额外的空间
            right = len(self.src)-1-self.sample_num_used
            # index:在sample_left里面的下标,因为有swap操作,所以index不一定等于idx
            # idx:在src数组中的下标
            for index,(idx,item) in enumerate(self.samples_left[:(len(self.src)-self.sample_num_used)]):
                if idx not in sample_idx:
                    continue
                else:
                    # swap
                    while self.samples_left[right][0] in sample_idx:
                        right-=1
                    if right<=index:
                        break
                    tmp = self.samples_left[index]
                    self.samples_left[index] = self.samples_left[right]
                    self.samples_left[right]=tmp
                    right-=1
            self.sample_num_used+=sample_num
        return self.samples_res
        


# a=[{'1':2},{'2':3,'4':-1},{'1':3,'5':0},{'a':2},{'1':90,'b':-9},{'c':7},{'d':9}]

# print(f'src:{a}')
# sample_list=[2,2,1]
# t = multi_random_sample(a,sample_list)
# samples_res=t.run()
# print(f'res:{samples_res}')

