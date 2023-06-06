import yaml
import os
import pandas as pd
import json
import random
import tensorflow.compat.v1 as tf
import pdb

def get_yaml_data(yaml_file):
    yaml_file = open(yaml_file, 'r')
    file_data = yaml_file.read()
    yaml_file.close()
    data = yaml.load(file_data,Loader=yaml.FullLoader)
    return data

def TrainTestSplit(fpath):
    fnames = tf.io.gfile.listdir(fpath)
    files=[ fpath+"/"+fn for fn in fnames if fn.startswith("part")]
    # random.shuffle(files)
    train_filename = files[:40]#本地测试
    test_filename = files[40:50]#本地测试
    # train_filename = files
    # test_filename = []
    return train_filename, test_filename

current_path = os.path.abspath('.')
yaml_path = os.path.join(current_path, 'config.yaml')
Configs = get_yaml_data(yaml_path)
train_filenames, eval_filenames = TrainTestSplit(Configs['fpath'])
demo_path = os.path.join(current_path,'demo_add_feature_newID_deviceID_feature.csv') #newId
# demo_path = os.path.join(current_path,'demo_add_feature.csv')
data = pd.read_csv(demo_path, nrows=5,delimiter='\t')
feature_size = data.columns.shape[0]-5
# COLUMNS = [data.columns[0]]+data.columns[3:-1].tolist()
COLUMNS = data.columns[4:-1].tolist() #newId
