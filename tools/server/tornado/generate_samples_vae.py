import torch
import os
import numpy as np 
from modules import VAE
from torchvision.utils import save_image
import base64

class VAE_TORCH():
        def __init__(self,model_path,gpu_id):
                self.Z_DIM = 128
                self.INPUT_DIM = 1
                self.DIM = 256
                self.model_path = model_path
                os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
                self.model = VAE(self.INPUT_DIM,self.DIM,self.Z_DIM).cuda()
                self.model.load_state_dict(torch.load(self.model_path))
                self.model.eval()
        def generate(self):
                z = torch.randn(1,self.Z_DIM,1,1).cuda()
                with torch.no_grad():
                    sample = self.model.decoder(z)
                    image = (sample.cpu().data+1)/2
                    return image
                

if __name__=='__main__':
        vae_torch = VAE_TORCH('./model/FashionMNIST_vae.pt',0)
        image = vae_torch.generate()
        save_image(image,'1.png')
        #p = image.numpy().tolist()
        #import json
        #res = {}
        #res['data'] = p
        #j = json.dumps(res)
        #import cv2
        #retval, buffer = cv2.imencode('.jpg', image_array)
        #pic_str = base64.b64encode(buffer)
        #pic_str = pic_str.decode()


