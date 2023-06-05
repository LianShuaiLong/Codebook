import gradio as gr
from diffusers import StableDiffusionInpaintPipelineLegacy
import torch
from PIL import Image
import numpy as np
from torchvision import transforms
import torch.nn.functional as F
import torch.nn as nn

# sam libs
from src.tools import *
from src.box_detection import *
from src.sam import *
# modnet libs
from src.modnet import *

import pdb

model_id = 'runwayml/stable-diffusion-v1-5'
pipe = StableDiffusionInpaintPipelineLegacy.from_pretrained(model_id,dtype=torch.float16)
pipe = pipe.to('cuda')
generator = torch.Generator("cuda").manual_seed(0)

sam_checkpoint = './models/sam_vit_b_01ec64.pth'
model_type = 'vit_b'
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam = sam.to('cuda')
predictor = SamPredictor(sam)

modnet_checkpoint = './models/modnet_photographic_portrait_matting.ckpt'
modnet = MODNet(backbone_pretrained=False)
modnet = nn.DataParallel(modnet).to('cuda')
modnet.load_state_dict(torch.load(modnet_checkpoint))
modnet.eval()

@torch.no_grad()
def image_inpainting(image,mask,invert_mask,background_prompt):
    if invert_mask:
        mask_array = np.asarray(mask)
        mask_array = 255-mask_array
        mask = Image.fromarray(mask_array.astype(np.uint8))
    outputs = pipe(
        prompt = [background_prompt],
        negative_prompt = ['(worst quality:0.7),3D,cartoon,illurstration'],
        image = image,
        mask_image=mask,
        num_inference_steps=25,
        strength=0.75,
        guidance_scale=7.5,
        num_images_per_prompt=1,
        generator=None).images
    output = outputs[0]
    return mask,output

@torch.no_grad()
def image_matting(image,type):
    #pdb.set_trace()
    if type=='car':
        box = get_car_boxes(image)
        mask, sam_score = box_prompt(box, image, predictor)
        mask = Image.fromarray(mask)
    elif type=='portrait':
        ref_size = 512
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
        ])
        img = transform(image)
        img = img[None,:,:,:]
        img_b,img_c,img_h,img_w = img.shape
        if max(img_h,img_w)<ref_size or min(img_h,img_w)>ref_size:
           if img_h>=img_w:
              img_rw = ref_size
              img_rh = int(img_h/img_w*ref_size)
           if img_h<=img_w:
              img_rh = ref_size
              img_rw = int(img_w/img_h*ref_size)
        else:
           img_rw = img_w
           img_rh = img_h

        img_rw = img_rw - img_rw%32
        img_rh = img_rh - img_rh%32
        im = F.interpolate(img,size=(img_rh,img_rw),mode ='area')

        _,_,matte = modnet(im.cuda(),True)

        matte = F.interpolate(matte,size=(img_h,img_w),mode ='area')
        matte = matte[0][0].data.cpu().numpy()
        mask = Image.fromarray(((matte * 255).astype('uint8')), mode='L')
    else:
        mask = image
    return mask

def README(param1,param2):
    txt1 = 'Functions so far:\n\tImage matting and Image background replace\n'
    txt2 = "Image matting:\n\tSAM for car Image matting\n\tModNet for portrait Image matting\n\tModNet Blog:\nhttps://zhuanlan.zhihu.com/p/344985719\n"
    txt3 = "Image edit:\n\tBased on blend lantent diffusion,generate image iteratively\n\tyou can try more times if the result is not satisfying\n\tBlend latent diffusions Blog:\nhttps://zhuanlan.zhihu.com/p/632643263\n"
    txt4 = "You can save 'output' for every function!\n"
    txt5 = "Be careful for that you should check 'invert mask' checkbox if you attempt to use 'Image background replace' func!"
    txt = txt1+txt2+txt3+txt4+txt5
    return txt

def launch():
    images = gr.inputs.Image(type='pil',label='source image')
    masks = gr.inputs.Image(type='pil',label='mask\nwhite region:region to edit')
    checkbox = gr.inputs.Checkbox(label='invert mask')
    background = gr.inputs.Textbox(label='prompt of desired background,such as "sunbeach,endless yellow sand,majestic ice moutain,doomsday city"')
    outputs = gr.inputs.Image(label='outputs with desired background')
    output_mask = gr.inputs.Image(label='invert mask result')
    app_bg_replace = gr.Interface(fn=image_inpainting,
                             inputs = [
                                 images,
                                 masks,
                                 checkbox,
                                 background
                             ],
                             outputs=[
                                 output_mask,
                                 outputs
                                 ],
                             examples=[['autohome.jpg','hhh.jpg',False,'majestic ice moutain']])

    
    image = gr.inputs.Image(label='image')
    Dropdown = gr.inputs.Dropdown(
        choices=['car','portrait'],
        type="value",
        default="car",
        label="mask type"
    )
    output = gr.inputs.Image(type='pil',label='masks')
    
    app_matting = gr.Interface(fn = image_matting,
            inputs=[
                image,
                Dropdown
            ],
            outputs=output
            )
    txt = gr.inputs.Textbox(placeholder='Show description of this gradio app',label='Introduction')
    description = gr.inputs.Textbox(placeholder='Description of this gradio app',label='Description')
    ThingsTodo = gr.inputs.CheckboxGroup(["dragGAN"],label='Tasks to do')
    app_README = gr.Interface(
            fn = README,
            inputs=[
                txt,
                ThingsTodo
                ],
            outputs=[
                description
                ]
            )

    apps = gr.TabbedInterface([app_README,app_matting,app_bg_replace],['README','Image matting','Image Edit'],title="Ellen's algorithm hub")
    apps.launch(server_name='0.0.0.0',server_port=8001,share=True)

if __name__=='__main__':
    launch()
