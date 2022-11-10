from multiprocessing import Process, Queue, set_start_method, Event
import logging
import sys
import json
import time
import requests
import logging
import base64

def download_file(url,pic_name,dst_dir):
    response = requests.get(url)
    img = response.content
    with open(f'{dst_dir}/{pic_name}','wb') as f:
        f.write(img)
    print(f'{dst_dir}/{pic_name} download successfully...')

class FileReader(Process):
    def __init__(self, fpath, out_que: Queue, name: str):
        Process.__init__(self)
        self.out_que = out_que
        self.name = name
        self.fpath = fpath
    

    def run(self):
        lines = open(self.fpath, encoding='utf-8').readlines()
        for line in lines[1:]:
            secs = line.strip('\n').split('\t')
            self.url = secs[0][1:]
            self.series_name = secs[1]
            self.spec_name = secs[2]
            self.pic_id = secs[3]
            self.pic_name = '_'.join([self.series_name,self.spec_name,self.pic_id,'.jpg'])
            self.pic_name = self.pic_name.replace(' ','')
            self.url = 'https://car0.autoimg.cn'+self.url
            self.out_que.put((self.url,self.pic_name))

class FileDownloader(Process):
    def __init__(self, in_que: Queue, out_que: Queue, stop_flag: Event, name: str,des_dir:str):
        Process.__init__(self)
        self.in_que = in_que
        self.out_que = out_que
        self.stop_flag = stop_flag
        self.name = name
        self.des_dir = des_dir
    def run(self):
        while not (self.stop_flag.is_set() and self.in_que.empty()):
            fid = None
            try:
                url,pic_name= self.in_que.get(timeout=10)
                download_file(url,pic_name,self.des_dir)
            except:
                continue
            
            


if __name__=='__main__':
    raw_que = Queue(100000)
    res_que = Queue(100000)

    global read_done
    read_done = Event()
    global reg_done
    reg_done = Event()

    pp1 = [FileReader('sql.res.log.1', raw_que, 'read_%d' % i) for i in range(1)]
    pp2 = [FileDownloader(raw_que, res_que, read_done, 'reg_%d' % i,'data.autohome.1') for i in range(5)]


    for p in pp1:
        p.start()
    for p in pp2:
        p.start()

    for p in pp1:
        p.join()
    read_done.set()
    for p in pp2:
        p.join()
    
    print('all done')
