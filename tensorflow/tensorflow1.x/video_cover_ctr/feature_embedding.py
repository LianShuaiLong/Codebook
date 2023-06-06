from utils import Configs
import json
import tensorflow.compat.v1 as tf

def _feature_column(columns):
    feature_setting_dict =  json.loads(open(Configs['feature_setting'],'r',encoding='utf-8').read())
    k = Configs['train']['k']
    deep_tower = []
    shallow_tower = []
    bias_tower = []
    
    for column in columns:
        # if column=='cover_layout':
        #     k=1
        # elif column == 'cover_vit_class':
        #     k=2
        feature_type = feature_setting_dict[column]['feature_type']
        process_method = feature_setting_dict[column]['process_method']
        feature_data_type = feature_setting_dict[column]['feature_data_type']
        tower_type = feature_setting_dict[column]['tower_type']

        # feature data type setting
        d_type = ''
        if feature_data_type=='string':
            d_type = tf.string
        elif feature_data_type=='int':
            d_type = tf.int64
        
        if feature_type == 'category':
            if tower_type=='shallow_tower':
                vocabulary_list = feature_setting_dict[column]['vocabulary_list']
                category_column = tf.feature_column.categorical_column_with_vocabulary_list(
                                        column,vocabulary_list,dtype=d_type,default_value=-1)
                # one hot encoding(sparse tensor)->multi hot encoding(dense tensor), go test for detail
                indicator_column = tf.feature_column.indicator_column(category_column)
                shallow_tower.append(indicator_column)
            elif tower_type == 'deep_tower':
                if process_method=='vocabulary_list':
                    vocabulary_list = feature_setting_dict[column]['vocabulary_list']
                    category_column = tf.feature_column.categorical_column_with_vocabulary_list(
                                        column,vocabulary_list,dtype=d_type,default_value=-1)
                    embedding_column = tf.feature_column.embedding_column(category_column,k+1)
                else:   #process_method=='hash_bucket':
                    hash_bucket_size = feature_setting_dict[column]['bucket_size']
                    hash_bucket_column = tf.feature_column.categorical_column_with_hash_bucket(
                        column,hash_bucket_size,dtype=d_type)
                    embedding_column = tf.feature_column.embedding_column(hash_bucket_column,k+1)
                deep_tower.append(embedding_column)
            else: #tower_type=='bias_tower': 
                # process_method='vocabulary_list' for default
                # hash_bucket_size = feature_setting_dict[column]['bucket_size']
                # hash_bucket_column = tf.feature_column.categorical_column_with_hash_bucket(
                #         column,hash_bucket_size,dtype=d_type)
                # # embedding_column = tf.feature_column.embedding_column(hash_bucket_column,k+1)
                # # embedding_column = tf.feature_column.embedding_column(hash_bucket_column,1) #直接one-hot到1维度输出
                # embedding_column = tf.feature_column.embedding_column(hash_bucket_column,30,initializer=tf.keras.initializers.RandomUniform(minval=-0.25, maxval=0.25, seed=1024)) #修改embedding的初始化方式
                # bias_tower.append(embedding_column)
                # device_id feature代替device_id(原值)
                numeric_column = tf.feature_column.numeric_column(column) # feature_type='category'是暂时的
                bias_tower.append(numeric_column)
                
        elif feature_type == 'dense': #e.g. ViT embedding or Bert embedding
            numeric_column = tf.feature_column.numeric_column(column)
            if process_method == 'bucket':
                buckets =  feature_setting_dict[column]['bucket']
                if float('-inf') in buckets:
                    boundary_dict = sorted(buckets[1:-1])
                else:
                    boundary_dict = buckets
                bucket_column = tf.feature_column.bucketized_column(numeric_column,boundary_dict)
                indicator_column = tf.feature_column.indicator_column(bucket_column)
                shallow_tower.append(indicator_column)
                # embedding_column = tf.feature_column.embedding_column(bucket_column,k+1)
            # else:
            #     embedding_column = numeric_column
            # if tower_type == 'deep_tower':
            #     deep_tower.append(embedding_column)
            # elif tower_type == 'shallow_tower':
            #     shallow_tower.append(embedding_column)
            # else:
            #     bias_tower.append(embedding_column)

        else:
            print('未知特征类型',column,feature_type)
    
    return deep_tower,shallow_tower,bias_tower
