import json
import os.path
import logging
import logging.handlers
import tornado
import tornado.web
import requests,base64
from generate_samples_vae import VAE_TORCH
import argparse
from tornado.options import options,define
import base64

log_dir='log/'
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
logging.basicConfig()
logger=logging.getLogger('info')
formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s\t', "%Y-%m-%d %H:%M:%S")
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(log_dir+'yearid_reg','D',30,0)
filehandler.suffix="%Y%m%d.log"
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

def generate_sample():
    sample = vae_torch.generate().squeeze(0)
    result = {}
    result['sample'] = sample.numpy().tolist()
    return result

class IndexHandler(tornado.web.RequestHandler):
    def post(self):
        """recive image , return recog result
        """
        try:
            result = json.loads(self.request.body)
        except ValueError:
            self.write({'returncode':10001, 'message':'recive body error'})
            logger.error(str({'returncode':10001, 'message':'recive body error'}))
            return None

        if 'uuid' in result:
            uuid = result['uuid']
        else:
            self.write({'returncode':10002, 'message':'result has no uuid or image_base64'})
            logger.error(str({'returncode':10002, 'message':'result has no uuid or image_base64'}))
            return None

        if 'random_code' in result:
            #imgobjfile = base64.b64decode(result['image_base64'])
            del result['random_code']
        else:
            self.write({'returncode':10002, 'message':'response error'})
            logger.error(str({'returncode':10002, 'message':'response error'}))
            return None
        # recognize
        logger.info("entrance" + "\t" + uuid)
        #try:
        result = generate_sample()
        #except:
        #    self.write({'returncode':10004, 'message':'generate error'})
        #    logger.error(str({'returncode':10002, 'message':'generate error'}))
        #    return None
        self.write(json.dumps(result))
        logger.info(json.dumps(result))
        self.finish()

def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path',type=str,default='./model/FashionMNIST_vae.pt')
    parser.add_argument('--port',type=int,default=80)
    parser.add_argument('--gpu_id',type=int,default=1)
    args = parser.parse_args()
    return args

if __name__=='__main__':
    args = parse_parser()

    vae_torch = VAE_TORCH(args.model_path,args.gpu_id)
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_id)
    app = tornado.web.Application(
        handlers=[(r'/generate_sample_demo', IndexHandler),],
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()


    
