import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

color_pxl = (255, 144, 255)
crop_size = (1024, 768)

def show_box(im, box):
    st = (int(box[0]), int(box[1]))
    ed = (int(box[2]), int(box[3]))
    im = cv2.rectangle(im, st, ed, (255, 0, 0, 1), 2)   # image, start point, endpoint, color, thickness
    return im

def show_mask(mask, picpath, box, print_box=False, outname='./output/res.jpg'):
    im = cv2.imread(picpath)

    mask_im = im.copy()
    mask_im[mask==True] = color_pxl
    mask_im[mask==False] = (0, 0, 0)

    final_im = mask_im*0.5 + im

    if print_box:
        final_im = show_box(final_im, box)
    cv2.imwrite(outname, final_im)

def crop_bg(impath):
    image = Image.open(impath)
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = image.crop(bbox)
        im.save(impath)

def resize_mask(mask, picpath, outname='./output/res.png'):
    outname = outname.replace('.jpg', '.png')

    # crop out the car
    im = cv2.imread(picpath)
    mask_im = im.copy()
    mask_im = cv2.cvtColor(mask_im, cv2.COLOR_BGR2BGRA)
    mask_im[mask==False] = (255, 255, 255, 0)
    cv2.imwrite(outname,mask_im)
    crop_bg(outname)

    # resize/add white boundary
    mask_im = cv2.imread(outname, cv2.IMREAD_UNCHANGED)
    curh, curw, _ = mask_im.shape
    neww, newh = resize_pic(curw, curh, 850, 740)
    mask_im = cv2.resize(mask_im, (neww, newh))
    h, w, _ = mask_im.shape

    im = np.ones((crop_size[1], crop_size[0], 4), dtype = np.uint8)
    im[:] = (255,255,255,0)

    x_pad = int((crop_size[0]-w)/2)
    y_pad = int((crop_size[1]-h)/2)

    im[y_pad:y_pad+h, x_pad:x_pad+w] = mask_im
    cv2.imwrite(outname, im)

def resize_pic(curw, curh, maxw=crop_size[0], maxh=crop_size[1]):
    if maxw/maxh > curw/curh:
        newh = maxh
        neww = (curw/curh)*newh
    else:
        neww = maxw
        newh = (curh/curw)*neww
    return int(neww), int(newh)
