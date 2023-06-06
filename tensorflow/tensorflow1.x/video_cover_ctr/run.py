import tensorflow.compat.v1 as tf
from utils import Configs, train_filenames, eval_filenames, COLUMNS, feature_size
from model import model_fn, make_input_fn
import json
import os
# import horovod.tensorflow as hvd #本地测试
import time
import random
import datetime
from feature_embedding import _feature_column
import pdb


if not os.path.exists(Configs['model_dir']):
    os.makedirs(Configs['model_dir'])

flags = tf.app.flags
flags.DEFINE_boolean("use_gpu", False, "Whether to use gpu training")
flags.DEFINE_boolean("is_train", True, "Whether is to be training")
flags.DEFINE_boolean("is_eval", True, "Whether is to be evaling")

FLAGS = flags.FLAGS

use_gpu = FLAGS.use_gpu
is_train = FLAGS.is_train
is_eval = FLAGS.is_eval


def export_model(model, path='export2'):
    column_names = model.params['feature_deep_tower']
    column_names += model.params['feature_shallow_tower']
    column_names += model.params['feature_bias_tower']
    #columns = []
    columns = set()
    feature_setting_dict = json.loads(open(Configs['feature_setting'],'r',encoding='utf-8').read())
    for line in column_names:
        if hasattr(line, "key"):
            line = line
            #print('line:',line.key,line.dtype)
            columns.add((line.key,line.dtype))
        elif hasattr(line.categorical_column, "key"):
            line = line.categorical_column
            #print('line:',line.key,line.dtype)
            columns.add((line.key,line.dtype))
        elif hasattr(line.categorical_column,"keys"):
            line = line.categorical_column.keys
            for k in line:
                line_k = k.source_column
                #print('line_K:',line_k.key,line_k.dtype)
                columns.add((line_k.key,line_k.dtype))
        else:
            line = line.categorical_column.source_column
            #print('line:',line.key,line.dtype)
            columns.add((line.key,line.dtype))
        #columns.append((line.key, line.dtype))
        #columns.add((line.key,line.dtype))
        
    tf.disable_eager_execution()
    feature_placeholders = {
        name: tf.placeholder(dtype, [1], name=name)
        for name, dtype in columns
    }
    export_input_fn = tf.estimator.export.build_raw_serving_input_receiver_fn(
        feature_placeholders)
    current_path = os.path.abspath('.')
    path = os.path.join(current_path,path)
    os.makedirs(path,exist_ok=True)
    path = model.export_saved_model(path, export_input_fn)


def TrainFileSplit(filenames,hvd_rank,hvd_size):
    
    while(len(filenames)<hvd_size):
        filenames=filenames+filenames
    size=len(filenames)
    res = size%hvd_size
    if res!=0:
        filenames=filenames[:size-res]
    files = [filenames[i] for i in range(len(filenames)) if i%hvd_size == hvd_rank]
    return files


def main(unused_argv):
    # hvd.init() #本地测试
    tf.logging.set_verbosity(tf.logging.INFO)
    # print("local_rank:",hvd.local_rank()) #本地测试
    # print("rank:",hvd.rank()) #本地测试
    
    # pdb.set_trace()
    deep_tower,shallow_tower,bias_tower = _feature_column(COLUMNS)


    params = {'feature_deep_tower': deep_tower,
             'feature_shallow_tower':shallow_tower,
             "feature_bias_tower":bias_tower,
             'feature_size': feature_size}
    params.update(Configs['train'])

    time_stamp = datetime.datetime.now()
    time_date = '-'.join([str(time_stamp.year),str(time_stamp.month),str(time_stamp.day)])
    model_dir = '{}/{}'.format(Configs['model_dir'],time_date)

    # model_dir = model_dir if hvd.rank() == 0 else None #本地测试
    model_dir = Configs['model_dir']
    
    config = tf.estimator.RunConfig(
        save_checkpoints_steps = 2000,
        save_summary_steps = 2000,
        keep_checkpoint_max = 10,
        log_step_count_steps = 100,
        #session_config=session_config, #本地测试
    )
    # bcast_hook = hvd.BroadcastGlobalVariablesHook(0)#本地测试
    estimator = tf.estimator.Estimator(model_fn=model_fn, model_dir=model_dir, params=params, config=config)
    eval_input_fn = make_input_fn(eval_filenames, batch_size=Configs['batch_size'], num_epochs=1, shuffle=False)
    # train_files=TrainFileSplit(train_filenames,hvd.rank(),hvd.size())#本地测试
    # eval_files=TrainFileSplit(eval_filenames,hvd.rank(),hvd.size())#本地测试
    train_files=train_filenames
    eval_files=eval_filenames
    time_duration=''
    if is_train:
        random.shuffle(train_files)
        time_start = datetime.datetime.now()
        # estimator.train(input_fn=make_input_fn(train_files, batch_size=Configs['batch_size'], num_epochs=None, shuffle=Configs['shuffle'], num_workers=hvd.size(), hvd_index=hvd.rank()), steps=Configs['steps'],hooks=[bcast_hook])
        estimator.train(input_fn=make_input_fn(train_files, batch_size=Configs['batch_size'], num_epochs=12, shuffle=Configs['shuffle']), steps=None)#本地测试
        time_end = datetime.datetime.now()
        time_duration = str((time_end-time_start).seconds)
        export_model(estimator, Configs["serving_model"])#本地测试

    if is_eval:
       print(eval_files)
       print('_'*50)
       print(train_files)
       random.shuffle(eval_files)
       #本地测试
    #    results = estimator.evaluate(input_fn=make_input_fn(eval_files, batch_size=Configs['batch_size'], num_epochs=1, shuffle=Configs['shuffle'], num_workers=hvd.size(), hvd_index=hvd.rank()), steps=None,hooks=[bcast_hook])
       results = estimator.evaluate(input_fn=make_input_fn(eval_files, batch_size=Configs['batch_size'], num_epochs=1, shuffle=Configs['shuffle']), steps=None)
       print("eval result:", results)
    #    results_list = [results['ctr_accuracy'],results['ctr_auc'],results['loss_mean']]
       #本地测试
    #    results_list = hvd.allreduce(tf.convert_to_tensor(results_list, dtype=tf.float32)).numpy().tolist()
    #    results['ctr_accuracy'] = results_list[0]
    #    results['ctr_auc'] = results_list[1]
    #    results['loss_mean'] = results_list[2]
    #    print("eval result avg:", results)

       results_train = estimator.evaluate(input_fn=make_input_fn(train_files, batch_size=Configs['batch_size'], num_epochs=1, shuffle=Configs['shuffle']), steps=None)
       
    #    results_train_list = [results_train['ctr_accuracy'],results_train['ctr_auc'],results_train['loss_mean']]
       
    #    results_train['ctr_accuracy'] = results_train_list[0]
    #    results_train['ctr_auc'] = results_train_list[1]
    #    results_train['loss_mean'] = results_train_list[2]
       print("train result:", results_train)

       
    #    ple_results = 'ple_eval_{}_epoch_0'.format(time.strftime('%Y%m%d%H%M%S', time.localtime()))

    #    for key in sorted(results):
    #        print('{}: {}'.format(key, results[key]))
    #        ple_results = ple_results + '_{}_{}'.format(key, str(results[key]))
    
    #本地测试
    # if hvd.rank()==0:
    #    os.system('curl "http://smsapi.in.autohome.com.cn/api/sms/send?_appid=sou&mobile=13321138921&message={}&fields=response"'.format(ple_results))

    # #本地测试
    # # if hvd.rank()==0:
    #     # sampleSize = os.popen("hadoop fs -du -h -s " + Configs['fpath']+"|awk '{print $1}'").read()
    #     # sampleNum = os.popen('hadoop fs -cat ' + Configs['fpath'] + '/* | wc -l').read()
            
    #     # time_stamp = datetime.datetime.now()
    #     # t1 = '-'.join([str(time_stamp.year),str(time_stamp.month),str(time_stamp.day)])
    #     # t2 = '-'.join([str(time_stamp.hour),str(time_stamp.minute),str(time_stamp.second)])
    #     # timeCreated = '_'.join([t1,t2])

    #     # Configs['serving_model']='{}/{}'.format(Configs['serving_model'],timeCreated)


    #     # export_model(estimator, Configs["serving_model"])

    #     model_pb = '{}/*/saved_model.pb'.format(Configs['serving_model'])
    #     savedModelpbSize = os.popen("hadoop fs -du -s -h {}".format(model_pb)).read()
    #     savedModelpbSize = savedModelpbSize.rsplit(' ',1)[0]
    #     model_md5 = os.popen("hadoop fs -cat {} | md5sum ".format(model_pb)).read()
    #     model_md5 = model_md5.split()[0]
    #     os.popen('hadoop fs -cp {}/*/* {}/'.format(Configs['serving_model'],Configs['serving_model']))


    #     # sampleSize, sampleNum = sizeOfDataDir(Configs["fpath"])
    #     # print(sampleSize)
    #     # print(sampleNum)

    #     with open(Configs["model_name"] + ".meta", "a+") as f:
    #         # f.write("auc: " + str(results["ctr_auc"]) + "\n")
    #         # f.write("loss: " + str(results["loss_mean"]) + "\n")
    #         # f.write("sampleSize: " + str(sampleSize) + "\n")
    #         # f.write("sampleNum: " + str(sampleNum) + "\n")
    #         f.write("auc: " + str(results["ctr_auc"]) + "\n")
    #         f.write("loss: " + str(results["loss_mean"]) + "\n")
    #         f.write("md5: " + str(model_md5)+"\n")
    #         f.write("zipFileName: "+Configs["model_name"]+".zip"+"\n")
    #         f.write("savedModelpbSize: "+str(savedModelpbSize)+"\n")
    #         f.write("timeCreated: " + str(timeCreated)+"\n")
    #         f.write("sampleSize: " + str(sampleSize))#+ "\n"
    #         f.write("sampleNum: " + str(sampleNum))# + "\n"
    #         f.write("isTenMin: False")
    #         f.write("trainingTime: "+time_duration+"s")
    #     os.popen('hadoop fs -put ' + Configs['model_name'] + ".meta " + Configs['serving_model'] ).read()

    #     # print(params['learning_rate'])
    #     # print(params)
    return results

if __name__ == "__main__":
    tf.app.run(main=main)
