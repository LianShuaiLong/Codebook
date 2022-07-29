import tensorrt as trt
import os
import sys
import cv2
import numpy as np
import pdb

'''
    engine: 推理用到的模型
    builder: 用来构建engine
    config:
    parser: 用来解析onnx文件
'''
sys.path.append('/workspace/tensorrt/samples/python')#common 文件的位置
import common
TRT_LOGGER = trt.Logger()
def get_engine(onnx_file_path,engine_file_path):
    '''
    Attempts to load a serialized engine if available,
    otherwise build a new TensorRT engine as save it
    '''
    def build_engine():
        builder = trt.Builder(TRT_LOGGER)
        network = builder.create_network(common.EXPLICIT_BATCH) 
        config = builder.create_builder_config()
        parser = trt.OnnxParser(network,TRT_LOGGER)
        runtime = trt.Runtime(TRT_LOGGER)

        config.max_workspace_size = 1<<28 #256MB 最大内存占用,一般1G，trt特有的，一切与优化有关
        builder.max_batch_size = 1 # 推理的时候要保证batch_size<=max_batch_size

        # parse model file
        if not os.path.exists(onnx_file_path):
            print(f'onnx file {onnx_file_path} not found,please run torch_2_onnx.py first to generate it')
            exit(0)
        print(f'Loading ONNX file from path {onnx_file_path}...')
        with open(onnx_file_path,'rb') as model:
            print('Beginning ONNX file parsing')
            if not parser.parse(model.read()):
                print('ERROR:Failed to parse the ONNX file')
                for error in range(parser.num_errors):
                    print(parser.get_error(error))
                return None
        
        # Static input setting
        network.get_input(0).shape=[1,3,512,512]
        # Dynamic input setting 动态输入在builder里面设置
        # profile = builder.create_optimization_profile()
        # profile.set_shape('input',(1,3,224,224),(1,3,512,512),(1,3,1024,1024))#最小的尺寸,常用的尺寸,最大的尺寸,推理时候输入需要在这个范围内
        # config.add_optimization_profile(profile)

        print('Completed parsing the ONNX file')
        print(f'Building an engine from file {onnx_file_path}; this may take a while...')
        # plan = builder.build_serialized_network(network,config)
        # engine = runtime.deserialize_cuda_engine(plan)
        engine = builder.build_engine(network,config)
        print('Completed creating Engine')
        with open(engine_file_path,'wb') as f:
            # f.write(plan)
            f.write(engine.serialize())
        return engine

    if os.path.exists(engine_file_path):
        print(f'Reading engine from file {engine_file_path}')
        with open(engine_file_path,'rb') as f,trt.Runtime(TRT_LOGGER) as runtime:
            return runtime.deserialize_cuda_engine(f.read())
    else:
        return build_engine()


def main():
    # create trt engine for onnx-based portrait model

    onnx_file_path = 'u2net.onnx'
    trt_file_path = 'u2net.trt'

    image_path = 'test4.jpg'
    # proprocess image
    image = cv2.imread(image_path)
    height,width = image.shape[:2]
    if height>width:
        w_pad = int((height-width)/2)
        image = np.pad(image,((0,0),(w_pad,w_pad),(0,0)),mode='constant',constant_values=((255,255),(255,255),(255,255)))
    else:
        h_pad = int((width-height)/2)
        image = np.pad(image,((h_pad,h_pad),(0,0),(0,0)),mode='constant',constant_values=((255,255),(255,255),(255,255)))
    image = cv2.resize(image,(512,512))
    image = image/np.max(image)
    tmpImg = np.zeros((512,512,3))
    # BGR2RGB
    tmpImg[:,:,0]=(image[:,:,2]-0.406)/0.255
    tmpImg[:,:,1]=(image[:,:,1]-0.456)/0.224
    tmpImg[:,:,2]=(image[:,:,0]-0.485)/0.229
    tmpImg = tmpImg.transpose((2,0,1)).astype(np.float32)# HWC->CHW
    tmpImg = tmpImg[np.newaxis,:,:,:]#CHW->NCHW

    # pdb.set_trace()
    # get trt model
    engine = get_engine(onnx_file_path,trt_file_path)
    # do inference with trt engine
    context = engine.create_execution_context()
    inputs,outputs,bindings,stream = common.allocate_buffers(engine)
    print(f'Running inference on image {image_path}...')
    inputs[0].host = np.ascontiguousarray(tmpImg) #************************
    trt_outputs = common.do_inference_v2(context,bindings=bindings,inputs=inputs,outputs=outputs,stream=stream)[0]
    # pdb.set_trace()
    trt_outputs = np.reshape(trt_outputs,(512,512))
    # postprocess trt output
    trt_outputs = 1.0-trt_outputs
    trt_outputs_max = np.max(trt_outputs)
    trt_output_min = np.min(trt_outputs)
    trt_outputs = (trt_outputs-trt_output_min)/(trt_outputs_max-trt_output_min)

    trt_outputs = trt_outputs*255
    trt_outputs = np.clip(trt_outputs,0,255)

    cv2.imwrite('test4_trt.jpg',trt_outputs)

if __name__=='__main__':
    main()
