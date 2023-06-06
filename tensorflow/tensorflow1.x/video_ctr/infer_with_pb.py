# 预测的时候如何处理sparse_tensor,tf.placeholder(dtype,shape=[None,5])
# https://blog.csdn.net/zj360202/article/details/70243127
import tensorflow.compat.v1 as tf 
import argparse
import pandas as pd
import json
import os

test_batch_account = 5
batch_size=1

def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',type=str,default='./v0004_ds')
    parser.add_argument('--model_dir',type=str,default='./v0004_model')
    parser.add_argument('--feature_setting_file',type=str,default='./feature_setting_v0004_3.json')
    parser.add_argument('--feature_column_file',type=str,default='./v0004_demo.csv')#feature1,feature2,...,dur_label,label
    args = parser.parse_args()
    return args

def get_columns(feature_column_file):
    data = pd.read_csv(feature_column_file,nrows=2)
    global feature_size
    feature_size = data.columns.shape[0]-2
    COLUMNS = data.columns[:-2].tolist()
    return COLUMNS
    
def create_test_iterator(COLUMNS,filenames,feature_setting_file):
    def input_fn():
        def read_row(csv_row):
            #different version different default value
            global feature_size
            record_defaults = [[0.]] * (feature_size - 53) + [['']] * 25 +[[0.]]*28+ [[0.], [0]]
            row = tf.decode_csv(csv_row, record_defaults=record_defaults)
            feature_dict_old = dict(zip(COLUMNS,row[:-2]))
            feature_setting_dict = json.loads(open(feature_setting_file,'r').read())
            feature_dict_new={}
            for column,v in feature_dict_old.items():
                feature_type = feature_setting_dict[column]['type']
                data_type = feature_setting_dict[column]['data_type']
                if feature_type == 'category':
                    if data_type == 'int':
                        tmp = tf.strings.split([v],';')
                        tmpValues = tf.string_to_number(tmp.values,out_type=tf.int64)
                        v_new = tf.SparseTensor(tmp.indices, tmpValues, tmp.dense_shape)
                    else:
                        v_new = tf.strings.split(v, ";")
                else:
                    v_new = v
                feature_dict_new[column] = v_new
            return feature_dict_new,row[-1],row[-2]    
        dataset = tf.data.TextLineDataset(filenames)
        dataset = dataset.skip(1).map(lambda line: read_row(line),num_parallel_calls=tf.data.experimental.AUTOTUNE).batch(batch_size).repeat(1)
        dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        iterator = dataset.make_one_shot_iterator()
        ds = iterator.get_next()
        ds = (ds[0], {'label': tf.to_float(ds[1]), 'dur_label': tf.to_float(ds[2])})
        return ds 
    return input_fn


def infer(test_iterator,model_path):
    with tf.Session(graph = tf.Graph()) as sess:
        meta_graph = tf.saved_model.loader.load(sess,[tf.saved_model.tag_constants.SERVING],model_path)
        inputs_outputs_signature = list(meta_graph.signature_def.items())[0][1]
        output_tensor_names = []
        output_op_names = []

        for output_item in inputs_outputs_signature.outputs.items():
            output_op_name = output_item[0]
            output_op_names.append(output_op_name)

            output_tensor_name = output_item[1].name
            output_tensor_names.append(output_tensor_name)

        print('output_tensor_names:\n',output_tensor_names)
        
        #sess.run(tf.global_variables_initializer())# what a shame
        
        ds = test_iterator()#->input_fn
        tf.disable_eager_execution()
        for i in range(test_batch_account):
            test_x,test_y = sess.run(ds)
            feed_dict_map = {}
            for input_item in inputs_outputs_signature.inputs.items():
                input_op_Name = input_item[0]
                input_tensor_name = input_item[1].name
                try:
                    data = sess.run((tf.squeeze(tf.sparse_tensor_to_dense(test_x[input_tensor_name.split(':')[0]]),[0,1])))
                except:
                    data = test_x[input_tensor_name.split(':')[0]]
                feed_dict_map[input_tensor_name] = data.reshape(batch_size,-1)
            print(sess.run(output_tensor_names[0],feed_dict = feed_dict_map))

if __name__ == '__main__':
    args = parse_parser()
    data_dir = args.data_dir
    model_dir = args.model_dir
    feature_setting_file = args.feature_setting_file
    feature_column_file = args.feature_column_file

    global feature_size
    COLUMNS = get_columns(feature_column_file=feature_column_file)
    test_files = [os.path.join(data_dir,filename) for filename in os.listdir(data_dir) if filename.endswith('csv')]
    print('test_files:\n',test_files)
    iterator_test = create_test_iterator(COLUMNS=COLUMNS,filenames=test_files,feature_setting_file=feature_setting_file)
    infer(iterator_test,model_dir)

