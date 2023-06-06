# 第一：在checkpoint中，graph的结构是存储在 xxx.meta文件中的，而真正的变量参数是存储的data文件中；savedmodel其实也是类似的， xxx.pb 文件仅仅保存graph的结构，真正的变量是存储的variables里面的，
# 第二：但是也有不同的地方,xxx.pb文件还可以保存常量，所以我可以将变量的值转化为常量，也就是所谓的freezing，然后整个graph结构以及各个常量、变量的值都可以存储在一个 pb 文件中了；
# 第三：另外，pb文件还可以使用签名，方便graph的重构与恢复
# tf保存：
#       checkpoint模式
#       saved_model模式(包含pb和variables)
#       纯pb模式(frozen pb):
#       keras的h5格式
# https://zhuanlan.zhihu.com/p/113734249⭐
# 对pb(非freeze得到的pb)进行一系列操作:meta_graph,输入输出节点,weights,graph可视化
import tensorflow.compat.v1 as tf
#import tensorflow as tf
#predict_fn = tf.saved_model.load('./ple_model_video_v0005/')#tf2.x版本的加载方式https://www.coder.work/article/7550262
import argparse
import os
import sys

def parse_parser():
      parser = argparse.ArgumentParser()
      parser.add_argument('--model_file_path',type=str,default='./ple_model_video_v0003')
      parser.add_argument('--dst_file_name',type=str,default='')
      args = parser.parse_args()
      return args

def parse_pb(model_file_path,dst_metagraph_name,dst_weights_name,dst_nodes_name):
    #https://blog.csdn.net/qq_27825451/article/details/105866464
    # get weights from pb dir
    with tf.Session(graph=tf.Graph()) as sess:
      meta_graph = tf.saved_model.loader.load(sess,[tf.saved_model.tag_constants.SERVING],model_file_path)
      #metagraph
      # meta_graph.signature_def 是一个字典，通过item()转化成 [(key,value)]的列表
      # [0] 表示的获取整个signature的内容，即等价于上面的（"predict",inputs...outputs...）
      # [1] 表示获取签名的值，即同时包值inputs属性和outputs属性
      savedStdout = sys.stdout
      with open(dst_metagraph_name,'w') as f:
        sys.stdout = f
        print(meta_graph) 
      sys.stdout = savedStdout
      #https://qastack.cn/programming/36193553/get-the-value-of-some-weights-in-a-model-trained-by-tensorflow
      #weights
      vars = tf.trainable_variables()
      vars_vals = sess.run(vars)
      with open(dst_weights_name,'w') as f:
        f.writelines(['var:{},value:{}\n'.format(var.name,val) for var,val in zip(vars,vars_vals)])
      #pd nodes
      savedStdout = sys.stdout
      with open(dst_nodes_name,'w') as f:
        sys.stdout = f
        nodes = os.popen("saved_model_cli show --dir {}/ --all ".format(model_file_path))#https://www.cnblogs.com/ruiy/p/6422586.html 
        print(nodes.read())
      sys.stdout = savedStdout
      #可视化图结构
      #不同形式得到的pb，读取方式不一样:https://github.com/Microsoft/MMdnn/issues/342
      tf.disable_eager_execution()
      # sess = tf.Session(graph=tf.Graph())
      # tf.saved_model.loader.load(sess,[tf.saved_model.tag_constants.SERVING],model_file_path)
      summaryWriter = tf.summary.FileWriter('{}/log/'.format(model_file_path),sess.graph)
      os.system('tensorboard --logdir={}/log/ --port 6006'.format(model_file_path))


if __name__ =='__main__':
      args = parse_parser()
      assert args.model_file_path!='','missing parameter model_file_path '
      model_file_path = args.model_file_path
      dst_metagraph_name = '{}_metagraph.log'.format(args.dst_file_name) if args.dst_file_name else '{}/{}_metagraph.log'.format(model_file_path,model_file_path.rsplit('/',1)[-1])
      dst_weights_name = '{}_weights.log'.format(args.dst_file_name)  if args.dst_file_name else '{}/{}_weights.log'.format(model_file_path,model_file_path.rsplit('/',1)[-1])
      dst_nodes_name = '{}_nodes.log'.format(args.dst_file_name) if args.dst_file_name else '{}/{}_nodes.log'.format(model_file_path,model_file_path.rsplit('/',1)[-1])
      parse_pb(model_file_path,dst_metagraph_name,dst_weights_name,dst_nodes_name)


      # for fronzen protobuf TF model.pb model not model dir
      # def load_graph(trained_model):   
      #   with tf.gfile.GFile(trained_model, "rb") as f:
      #       graph_def = tf.GraphDef()
      #       graph_def.ParseFromString(f.read())

      #   with tf.Graph().as_default() as graph:
      #       tf.import_graph_def(
      #           graph_def,
      #           input_map=None,
      #           return_elements=None,
      #           name=""
      #           )
      #   return graph

      # for TF model using API SavedModelBuilder, model_dir 
      # export_dir = "./tf_resnet152"
      # with tf.Session(graph=tf.Graph()) as sess:
      #     tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.TRAINING], export_dir)

      #     x = sess.graph.get_tensor_by_name('input:0')
      #     y = sess.graph.get_tensor_by_name('xxxxxx:0')
      #     ......
      #     _y = sess.run(y, feed_dict={x: _x})
  
 