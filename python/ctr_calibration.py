import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ctr',type=float,default=1.0)
    parser.add_argument('--sample_rate',type=float,default=0.0,help='Negetive sample rate')
    args = parser.parse_args()
    return args

def calibration(ctr:float,r:float):
    """
    假设正样本数量N_p
    负采样之后负样本的数量N_n
    负采样率为r
    负采样之后ctr值为p(不经过负采样的话,模型会打压正样本)
    理论上的ctr值p'
    p/(1-p) = N_p/(N_n/r) = N_p/N_n*r
    p = 1/(1+math.pow(e,-wx))#假设最后全连接的偏置b=0,这部分可以结合为什么采用sigmoid作为二分类模型的激活函数
    ->math.log(p/(1-p)) = wx
    r*p'/(1-p') = N_p/N_n = p/(1-p)
    ->math.log(r)+math.log(p'/(1-p')) = wx
    ->p'/(1-p') = math.pow(wx-lnr)
    ->p' = 1/(1+math.pow(-(wx+math.log(r))))
    ->p' = p/(p+(1-p)/r)
    """
    return ctr/(ctr+(1-ctr)/r)

if __name__=='__main__':
    args = parse_args()
    ctr = args.ctr
    r = args.sample_rate 
    print(calibration(ctr=ctr,r=r))