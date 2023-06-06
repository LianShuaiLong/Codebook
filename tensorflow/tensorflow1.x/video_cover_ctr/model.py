import tensorflow.compat.v1 as tf
import os
from utils import feature_size, COLUMNS,Configs
# import horovod.tensorflow as hvd #本地测试
import json
import pdb



def isSparse(variable, fields):
    """ 判断变量是否为稀疏变量 """
    flag = False
    for filed in fields:
        if filed in variable.name:
            flag = True
            break
    return flag


def read_row(csv_row):
    # pdb.set_trace()
    # record_defaults = [['']] * 10+[[0.]]+[['']]*7 +[[0.]]# newId
    # record_defaults = [['']] * 9+[[0.]]+[['']]*7 +[[0.]]
    record_defaults = [['']] * 10+[[0.]]+[['']]*7 +[[0.]]*4 +[[0.]]# device_id feature
    
    # debug_value = tf.Print(csv_row,[csv_row])

    row = tf.decode_csv(csv_row, record_defaults=record_defaults,field_delim="\t")
    # feature_dict_old = dict(zip(COLUMNS,row[3:-1])) # newId
    # feature_dict_old = dict(zip(COLUMNS,[row[0]]+row[3:-1]))
    feature_dict_old = dict(zip(COLUMNS,row[4:-1])) # device_id feature
    feature_setting_dict = json.loads(open(Configs['feature_setting'],'r',encoding='utf-8').read())
    feature_dict_new={}
    for column,v in feature_dict_old.items():
        feature_type = feature_setting_dict[column]['feature_type']
        feature_data_type = feature_setting_dict[column]['feature_data_type']

        if feature_type == 'category':
            if feature_data_type == 'int':
                tmp = tf.strings.split([v],',')
                tmpValues = tf.string_to_number(tmp.values,out_type=tf.int64)
                v_new = tf.SparseTensor(tmp.indices, tmpValues, tmp.dense_shape)
            elif feature_data_type == 'string':
                # v_new = tf.strings.split(v, ",",result_type='RaggedTensor')
                tmp = tf.strings.split([v], ",")#,result_type='RaggedTensor') #https://stackoverflow.com/questions/62686600/attributeerror-tensor-object-has-no-attribute-to-sparse
                v_new = tf.SparseTensor(indices=tmp.indices,values=tmp.values,dense_shape=tmp.dense_shape)
            else:
                v_new = v
        else:
            v_new = v
        feature_dict_new[column] = v_new
    return feature_dict_new,row[-1]


def make_input_fn(filename, batch_size=128, shuffle=False, num_epochs=3, num_workers=3, hvd_index=0):
    def input_fn():
        with tf.name_scope("Inputs"):
            dataset = tf.data.TextLineDataset(filename)
            dataset = dataset.skip(1).map(lambda line: read_row(line), num_parallel_calls=tf.data.experimental.AUTOTUNE).batch(batch_size).repeat(num_epochs)
            dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

            iterator = dataset.make_one_shot_iterator()
            ds = iterator.get_next()
            ds = (ds[0], {'label': tf.to_float(ds[1])})
           
        return ds
    return input_fn

def model_fn(features, labels, mode, params):
    with tf.name_scope('shallow_tower'):
        feature_shallow_tower = tf.feature_column.input_layer(features,params['feature_shallow_tower'])
        feature_field_size = Configs['train']['tower_width'][-1]/2 #len(params['feature_shallow_tower'])
        shallow_feature = tf.keras.layers.Dense(feature_field_size,activation=None)(feature_shallow_tower)
        shallow_feature = tf.layers.batch_normalization(shallow_feature, training=mode==tf.estimator.ModeKeys.TRAIN, axis=1)
        shallow_feature = tf.nn.relu(shallow_feature)
    
    with tf.name_scope('bias_tower'):
        feature_bias_tower = tf.feature_column.input_layer(features,params['feature_bias_tower'])
        # feature_field_size = len(params['feature_bias_tower'])
        bias_feature = tf.keras.layers.Dense(15,activation=None)(feature_bias_tower)
        bias_feature = tf.layers.batch_normalization(bias_feature, training=mode==tf.estimator.ModeKeys.TRAIN, axis=1)
        #bias_logits = tf.nn.leaky_relu(bias_feature)
        # add complexity
        bias_feature = tf.nn.leaky_relu(bias_feature)
        bias_feature = tf.keras.layers.Dense(1,activation=None)(feature_bias_tower)
        bias_feature = tf.layers.batch_normalization(bias_feature, training=mode==tf.estimator.ModeKeys.TRAIN, axis=1)
        bias_logits = tf.nn.leaky_relu(bias_feature)

        # one-hot
        # bias_feature = tf.keras.layers.Dense(1,activation=None)(feature_bias_tower)
        # bias_logits = feature_bias_tower

    with tf.name_scope('feature_embed'):
        feature_input = tf.feature_column.input_layer(features,params['feature_deep_tower'])
        feature_field_size = len(params['feature_deep_tower'])
    
    
    with tf.name_scope('CGC'):
        with tf.name_scope('Expert_A'):
            experts = []
            for expert in range(params['expert_num']):
                expert_t = feature_input
                for unit in params['expert_width']:
                    expert_t = tf.keras.layers.Dense(units=unit,activation=None)(expert_t)
                    if params['batch_norm']:
                        expert_t = tf.layers.batch_normalization(expert_t, training=mode==tf.estimator.ModeKeys.TRAIN, axis=1)
                    expert_t = tf.nn.relu(expert_t)
                experts.append(expert_t)
        
        with tf.name_scope('gate'):
            unit = Configs['train']['expert_num']
            gate = tf.keras.layers.Dense(units=unit,activation=None)(feature_input)
            gate = tf.expand_dims(gate,axis=1)
            gate = tf.nn.softmax(gate)
    

        # feature_task_ctr = tf.concat([Expert_A,Expert_S],axis=0)
        deep_expert_feature = tf.transpose(experts,[1,2,0])
        deep_expert_feature = tf.multiply(gate,deep_expert_feature)
        deep_expert_feature = tf.reduce_sum(deep_expert_feature,axis=2)

        with tf.name_scope('Tower'):
            for unit in Configs['train']['tower_width']:
                deep_feature =  tf.keras.layers.Dense(units=unit, activation=None)(deep_expert_feature)
                if Configs['train']['batch_norm']:
                    deep_feature = tf.layers.batch_normalization(deep_feature, training=mode==tf.estimator.ModeKeys.TRAIN, axis=1)
            deep_feature = tf.nn.relu(deep_feature)
   
            
    with tf.name_scope('output'):
        feature = tf.concat([shallow_feature,deep_feature],axis=1)
        # feature = deep_feature         
        # bias_feature = bias_tower_logit
        # feature = tf.math.add(feature,bias_feature)
        ctr_logits = tf.keras.layers.Dense(1,activation=None)(feature)
        ctr_logits = tf.squeeze(ctr_logits,[1])
        bias_logits = tf.squeeze(bias_logits,[1])
        ctr_logits = tf.add(ctr_logits,bias_logits)
        # ctr = tf.nn.sigmoid(tf.add(ctr_logits,bias_logits),name='ctr')
        # ctr = tf.nn.sigmoid(ctr_logits,name='ctr') #只使用device_id训练模型
        ctr = tf.nn.sigmoid(ctr_logits,name='ctr')

    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = {
         'ctr': ctr
        }
     
        return tf.estimator.EstimatorSpec(mode, predictions=predictions)

    with tf.name_scope('loss'):
        y = labels['label']
        # loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y, logits=ctr_logits), name="ctr_loss")
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y, logits=ctr_logits), name="ctr_loss")
        ctr_auc, ctr_auc_update = tf.metrics.auc(labels=y,predictions=ctr,name='ctr_auc')
        train_show_dict = {'ctr_auc': "loss/ctr_auc/value"}
        train_hook = tf.train.LoggingTensorHook(train_show_dict,every_n_iter=100)

        
    with tf.name_scope('metrics'):
        y = labels['label']
        ctr_accuracy = tf.metrics.accuracy(labels=y, predictions=tf.to_float(tf.greater_equal(ctr, 0.5)))
        ctr_auc = tf.metrics.auc(y, ctr)
        loss_mean = tf.metrics.mean(loss)

        metrics = {'ctr_accuracy': ctr_accuracy, 'ctr_auc': ctr_auc,'loss_mean':loss_mean}
       
    
    if mode == tf.estimator.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=metrics)

    assert mode == tf.estimator.ModeKeys.TRAIN, 'mode train must be true'

    # with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
    global_step=tf.train.get_global_step()
    # 获取所有可训练的变量
    trainable_variables = [variable for variable in tf.trainable_variables()]
    # 获取稀疏变量列表
    sparse_list = [x.name for x in params["feature_bias_tower"]#.all_columns.values() 
            if "EmbeddingColumn" in str(type(x)) and 
                "HashedCategoricalColumn" in str(type(x.categorical_column)) and 
                x.categorical_column.hash_bucket_size > 200000
            ]
    # pdb.set_trace()
    # 获取embedding变量
    embedding_variables = [variable for variable in trainable_variables if "embedding_weights" in variable.name]
    # print(embedding_variables)
    # 获取稀疏embedding变量
    embedding_sparse_variables = [variable for variable in embedding_variables if isSparse(variable, sparse_list)]
    # 获取稠密embedding变量
    embedding_dense_variables = [variable for variable in embedding_variables if variable not in embedding_sparse_variables]
    # 获取非embedding变量
    param_variables = [variable for variable in trainable_variables if variable not in embedding_variables]
    # 获取所有可训练变量
    # all_variables = [variable for variable in trainable_variables]
    # 定义稀疏变量优化器
    optimizer_sparse_emb = tf.train.AdagradOptimizer(learning_rate=0.1)
    #train_op_sparse_emb = optimizer_sparse_emb.minimize(loss, var_list=embedding_sparse_variables,global_step=global_step)
    # train_op_sparse_emb = optimizer_sparse_emb.minimize(loss, var_list=embedding_sparse_variables)
    # 定义稠密变量优化器
    optimizer_dense_emb = tf.train.AdagradOptimizer(learning_rate=0.001)
    train_op_dense_emb = optimizer_dense_emb.minimize(loss, var_list=embedding_dense_variables)
    # 定义全局变量优化器
    optimizer_param = tf.train.AdamOptimizer(learning_rate=params["learning_rate"])
    train_op_param = optimizer_param.minimize(loss, var_list=[param_variables+embedding_dense_variables], global_step=global_step)#非embedding变量和稠密embedding变量
    # 将所有优化器集合到一起
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    # train_op = tf.group(update_ops, train_op_sparse_emb, train_op_dense_emb, train_op_param)
    # train_op = tf.group(update_ops, train_op_sparse_emb, train_op_param)
    # train_op = tf.group(update_ops,train_op_sparse_emb, train_op_dense_emb, train_op_param,ctr_auc_update)
    train_op = tf.group(update_ops,train_op_dense_emb, train_op_param,ctr_auc_update)
                        


    # warmup_step=params['warmup_step']
    # linear_increase= params['learning_rate']*tf.cast(global_step/warmup_step,tf.float32)
    # exponential_decay=tf.train.polynomial_decay(learning_rate=params['learning_rate'], global_step=global_step-warmup_step, decay_steps=params["decay_steps"],end_learning_rate=params['end_learning_rate'], power=0.5, cycle=True)
    # learning_rate=tf.cond(global_step<=warmup_step,lambda:linear_increase,lambda:exponential_decay)
    # optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate )
    # # optimizer = hvd.DistributedOptimizer(optimizer) #本地测试
    # train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())

    return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op,training_hooks=[train_hook])
