#swing召回算法,代码借鉴 https://blog.csdn.net/Gamer_gyt/article/details/115678598
import json
import argparse
import pandas as pd
from itertools import combinations
from collections import defaultdict
import os

alpha = 0.5
topk=20

def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data_path',type=str,default='./swing-data/ml-100k/ua.base')
    parser.add_argument('--test_data_path',type=str,default='./swing-data/ml-100k/ua.test')
    parser.add_argument('--model_path',type=str,default='./swing-data/swing.json')
    args = parser.parse_args()
    return args

def load_data(train_data_path:str,test_data_path:str):
    train_data = pd.read_csv(train_data_path,sep = '\t',engine='python',names=['userid','movieid','rate','EventTimeStamp'])
    test_data = pd.read_csv(test_data_path,sep = '\t',engine='python',names=['userid','movieid','rate','EventTimeStamp'])

    print('train data example:\n',train_data.head(5))
    print('test data example:\n',test_data.head(5))

    return train_data,test_data

def get_iusers_uitems(train_data):
    i_users = defaultdict(set)
    u_items = defaultdict(set)
    for index,rows in train_data.iterrows():
        i_users[str(rows['movieid'])].add(str(rows['userid']))
        u_items[str(rows['userid'])].add(str(rows['movieid']))

    print('item个数:',len(i_users.keys()))
    print('user个数:',len(u_items.keys()))
    return i_users,u_items
        
def train(i_users:dict,u_items:dict):
    item_pairs = list(combinations(i_users.keys(),r=2))
    print('item pairs:\n',len(item_pairs))
    item_sim_dict = defaultdict(dict)
    
    item_pair = 0
    for item_i,item_j in item_pairs:
        print('当前item pair:',item_pair)
        result = 0
        common_users = i_users[item_i] & i_users[item_j]
        user_pairs = list(combinations(common_users,r=2))
        for user_i,user_j in user_pairs:
            result += 1/(alpha+len(u_items[user_i] & u_items[user_j]))
        item_sim_dict[item_i][item_j] = result
        item_pair+=1

    for k,v in item_sim_dict.items():
        item_sim_dict[k] = dict(sorted(item_sim_dict[k].items(),key=lambda k: k[1],reverse=True)[:topk])
    return item_sim_dict

def save_model(item_sim_dict:dict,model_path:str):
    with open(model_path,'w') as f:
        f.write(json.dumps(item_sim_dict,ensure_ascii=True,indent=4))
    print('模型{}-{}保存完成'.format(model_path,topk))


if __name__=='__main__':

    args = parse_parser()
    train_data_path = args.train_data_path 
    test_data_path = args.test_data_path
    model_path = args.model_path

    train_data,test_data = load_data(train_data_path,test_data_path)
    i_users,u_items = get_iusers_uitems(train_data=train_data)
    item_sim_dict = train(i_users=i_users,u_items=u_items)
    save_model(item_sim_dict=item_sim_dict,model_path=model_path)

