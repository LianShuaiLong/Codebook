from multiprocessing import Process, Queue, set_start_method, Event
import logging
import sys
import json
import time
import requests
import logging
import base64



def download_file(url):
    img = requests.get(url)
    return img

class FileReader(Process):
    def __init__(self, fpath, out_que: Queue, name: str):
        Process.__init__(self)
        self.out_que = out_que
        self.name = name
        self.fpath = fpath
        self.url = ''


    def run(self):
        with open(self.fpath, encoding='utf-8') as fin:
            for line in fin:
                self.url = line.strip('\n')
                try:
                   data = download_file(self.url)
                except Exception:
                    continue
                data = base64.b64encode(data.content).decode("ascii")
                self.out_que.put((self.url,data))

class FileProcessor(Process):
    def __init__(self, in_que: Queue, out_que: Queue, stop_flag: Event, name: str):
        Process.__init__(self)
        self.in_que = in_que
        self.out_que = out_que
        self.stop_flag = stop_flag
        self.name = name
    def run(self):
        while not (self.stop_flag.is_set() and self.in_que.empty()):
            fid = None
            try:
                url,data = self.in_que.get(timeout=10)
            except:
                continue
            res_dict = get_ocr_from_bml(data)
            self.out_que.put((url,res_dict))


class ResWriter(Process):
    def __init__(self, out_dir, in_que: Queue, stop_flag: Event, name: str):
        Process.__init__(self)
        self.in_que = in_que
        self.stop_flag = stop_flag
        self.name = name
        self.line_dict={}

    def run(self):
        while not (self.stop_flag.is_set() and self.in_que.empty()):
            try:
                url,res_dict = self.in_que.get(timeout=10)
                self.line_dict[url] = res_dict
            except:
                continue

            if len(self.line_dict) > 100:
                self.flush2file()

    def flush2file(self):
        t = time.time()
        f = open('edit_dist_0_with_keywords_{}.csv'.format(t), 'w')
        for url, res_dict in self.line_dict.items():
            res = [url,res_dict]
            f.write('%s\n' % json.dumps(res))
        f.close()
        self.line_dict={}

if __name__=='__main__':
    raw_que = Queue(100000)
    res_que = Queue(100000)

    global read_done
    read_done = Event()
    global reg_done
    reg_done = Event()

    pp1 = [FileReader('url_file.txt', raw_que, 'read_%d' % i) for i in range(1)]
    pp2 = [FileProcessor(raw_que, res_que, read_done, 'reg_%d' % i) for i in range(32)]
    pp3 = [ResWriter('rough_finder', res_que, reg_done, 'write_%d' % i) for i in range(1)]

    for p in pp1:
        p.start()
    for p in pp2:
        p.start()
    for p in pp3:
        p.start()

    for p in pp1:
        p.join()
    read_done.set()
    for p in pp2:
        p.join()
    reg_done.set()
    for p in pp3:
        p.join()
    print('all done')
