import argparse
import json
import pandas as pd
from itertools import combinations
from collections import defaultdict
from math import sqrt
topK=20
def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data_path',type=str,default='./swing-data/ml-100k/ua.base')
    parser.add_argument('--test_data_path',type=str,default='./swing-data/ml-100k/ua.test')
    parser.add_argument('--model_path',type=str,default='./swing-data/ml-100k-item_cf.json')
    args = parser.parse_args()
    return args

def load_data(train_data_path:str,test_data_path:str):
    train_data = pd.read_csv(train_data_path,sep='\t',engine='python',names=['userid','movieid','rate','eventtimestamp'])
    test_data = pd.read_csv(test_data_path,sep='\t',engine='python',names=['userid','movieid','rate','eventtimestamp'])

    print('train data example:\n',train_data.head(5))
    print('test data example:\n',test_data.head(5))

    return train_data,test_data

def get_iusers_uitems(train_data):
    i_users=defaultdict(set)
    u_items=defaultdict(set)

    for idx,row in train_data.iterrows():
        userid = str(row['userid'])
        itemid = str(row['movieid'])
        i_users[itemid].add(userid)
        u_items[userid].add(itemid)
    print('item数目:',len(i_users.keys()))
    print('user数目:',len(u_items.keys()))

    return i_users,u_items

def train(i_users:dict,u_items:dict):
    item_pairs = list(combinations(i_users.keys(),r=2))
    print('item pair数目:',len(item_pairs))
    item_sim_dict = defaultdict(dict)
    item_pair_idx = 0
    for item_i,item_j in item_pairs:
        print('当前item pair:',item_pair_idx)
        common_users = i_users[item_i] & i_users[item_j]
        item_i_users = i_users[item_i]
        item_j_users = i_users[item_j]
        result = '{:.2f}'.format(len(common_users)/sqrt(len(item_i_users)*len(item_j_users)))
        item_sim_dict[item_i][item_j] = result
        item_pair_idx+=1
    return item_sim_dict

def save_model(item_sim_dict:dict,model_path:str):
    for k,v in item_sim_dict.items():
        v_new = dict(sorted(v.items(),key=lambda k: k[1],reverse=True)[:topK])
        item_sim_dict[k] = v_new
    with open(model_path,'w') as f:
        f.write(json.dumps(item_sim_dict,ensure_ascii=True,indent=4))
    print('{}-{}保存成功'.format(model_path,topK))

if __name__=='__main__':
    args = parse_parser()
    train_data_path = args.train_data_path
    test_data_path = args.test_data_path
    model_path = args.model_path

    train_data,test_data = load_data(train_data_path=train_data_path,test_data_path=test_data_path)
    i_users,u_items = get_iusers_uitems(train_data=train_data)
    item_sim_dict = train(i_users=i_users,u_items=u_items)
    save_model(item_sim_dict=item_sim_dict,model_path=model_path)