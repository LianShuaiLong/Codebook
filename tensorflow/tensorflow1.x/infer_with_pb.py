import tensorflow.compat.v1 as tf 
import argparse
import pandas as pd
import json
data = pd.read_csv('./demo.csv', nrows=5)
feature_size = data.columns.shape[0]-2
COLUMNS = data.columns[:-2].tolist()
test_batch_account = 1

def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',type=str,default='./test_data')
    parser.add_argument('--model_dir',type=str,default='./ple_model_video_v0003')
    args = parser.parse_args()
    return args

def create_test_iterator(filenames):
    def input_fn():
        def read_row(csv_row):
            record_defaults = [[0.]] * (feature_size - 51) + [['']] * 25 +[[0.]]*26+ [[0.], [0]]
            row = tf.decode_csv(csv_row, record_defaults=record_defaults)
            feature_dict_old = dict(zip(COLUMNS,row[:-2]))
            feature_setting_dict = json.loads(open('feature_setting_v0002.json','r').read())
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
        dataset = dataset.skip(1).map(lambda line: read_row(line),num_parallel_calls=tf.data.experimental.AUTOTUNE).batch(1).repeat(1)
        dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        iterator = dataset.make_one_shot_iterator()
        # ds = iterator.get_next()
        # ds = (ds[0], {'label': tf.to_float(ds[1]), 'dur_label': tf.to_float(ds[2])})
        return iterator #ds
    return input_fn


def infer(test_iterator,model_path):
    with tf.Session(graph = tf.Graph()) as sess:
        #tf.disable_eager_execution()
        meta_graph = tf.saved_model.loader.load(sess,[tf.saved_model.tag_constants.SERVING],model_path)
        inputs_outputs_signature = list(meta_graph.signature_def.items())[0][1]

        output_tensor_names = []
        output_op_names = []

        for output_item in inputs_outputs_signature.outputs.items():
            output_op_name = output_item[0]
            output_op_names.append(output_op_name)

            output_tensor_name = output_item[1].name
            output_tensor_names.append(output_tensor_name)
        
        sess.run(tf.global_variables_initializer())
        #sess.run(test_iterator().initializer)
        #sess.run(test_iterator)
        
        
        tf.disable_eager_execution()
        for i in range(test_batch_account):
            x_test,y1_test,y2_test = test_iterator().get_next()
            x_test,y1_test,y2_test = x_test,tf.to_float(y1_test), tf.to_float(y2_test)
            test_x,test_y1,test_y2 = sess.run([x_test,y1_test,y2_test])
            feed_dict_map = {}
            for input_item in inputs_outputs_signature.inputs.items():
                input_op_Name = input_item[0]
                input_tensor_name = input_item[1].name
                feed_dict_map[input_tensor_name] = test_x[input_tensor_name.split(':')[0]]
            # for k,v in feed_dict_map.items():
            #     print(k,v)
            print(sess.run(output_tensor_names[0],feed_dict = feed_dict_map))
        
           

if __name__ == '__main__':
    args = parse_parser()
    data_dir = args.data_dir
    model_dir = args.model_dir
    iterator_test = create_test_iterator('./demo.csv')
    infer(iterator_test,model_dir)

