# 用于查询指定文件夹下面指定类型的文件
import argparse
import os
import zipfile

class FileSearcher(object):
    def __init__(self,file_type=[]):
        super(FileSearcher,self).__init__()
        self.file_type = set(file_type)
        self.file_search_res = []
    def search(self,path):
        if os.path.isfile(path):
            if path.rsplit('.')[-1] in self.file_type:
                self.file_search_res.append(path)
            return
        elif os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                self.search(os.path.join(path,file))
            return
        else:
            return

def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_type',type=str,default='py',help='要查找的文件类型,多种用,分隔')
    parser.add_argument('--root_path',type=str,default='./',help='根路径')
    args = parser.parse_args()
    return args

def main():
    args = parse_parser()
    file_type = args.file_type.split(',')
    print(f'查询文件类型:{file_type}')
    root_path = args.root_path
    fs = FileSearcher(file_type)
    fs.search(root_path)
    files = fs.file_search_res
    with zipfile.ZipFile('test.zip','w',compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f)

if __name__=='__main__':
    main()


