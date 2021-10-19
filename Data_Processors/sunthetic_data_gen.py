# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 16:54:31 2021

@author: talha
"""

from PIL import Image, ExifTags
import cv2, glob, os, re, PIL
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import tqdm, trange
from imgaug import augmenters as iaa
import imgaug as ia
import imgviz
from gray2color import gray2color
mpl.rcParams['figure.dpi'] = 300

from synth_utils import *


images_c = "D:/binary_seg_data/images/crops_90/"
images_w = "D:/binary_seg_data/images/weeds_90/"

masks_c = "D:/binary_seg_data/masks/crops_90/"
masks_w = "D:/binary_seg_data/masks/weeds_90/"

bgs = "D:/binary_seg_data/backgrounds/"

class_names = np.array(['bean', 'cockspur_grass', 'corn', 'e_oryzoides', 'fall_panicum',
                       'foxtail_millet', 'great_millet', 'green_foxtail', 'green_gram',
                       'indian_goosegrass', 'peanut', 'perilla', 'poa_annua',
                       'proso_millet', 'red_bean', 'rice_cockspur', 'sesame',
                       'southern_crabgrass'])


path2_images_c = get_all_images(images_c)
path2_images_w = get_all_images(images_w)
path2_masks_c = get_all_images(masks_c)
path2_masks_w = get_all_images(masks_w)
path2_bgs = get_all_images(bgs)

get_crops = 10
get_weeds = 10

idx = 0



bg_img = cv2.imread(path2_bgs[0], -1)
bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2RGB)

bg_mask = np.zeros(bg_img.shape)
h, w = bg_img.shape[:2]

#id2assign = get_sem_id(class_names, img_path)

indices_i = np.arange(len(path2_images_c))
indices_m = np.arange(len(path2_images_w))

np.random.shuffle(indices_i)
np.random.shuffle(indices_m)

inds_c = indices_i[idx * get_crops: (idx + 1) * get_crops]
inds_w = indices_m[idx * get_weeds: (idx + 1) * get_weeds]

batch_imgs_c = []
batch_imgs_w = []

batch_masks_c = []
batch_masks_w = []

ids2assign_c = []
ids2assign_w = []

for i in inds_c:
    img_c = img_reader(path2_images_c[i])
    img_c = img_c.resize((w, h), PIL.Image.BILINEAR)
    img_c = np.array(img_c)
    
    mask_c = cv2.imread(path2_masks_c[i], 1)
    mask_c = cv2.resize(mask_c, (w, h), interpolation = cv2.INTER_NEAREST) # masks
    ids2assign_c.append(get_sem_id(class_names, path2_masks_c[i]))
    
    batch_imgs_c.append(img_c)
    batch_masks_c.append(mask_c)
    
for j in inds_w:
    img_w = img_reader(path2_images_w[j])
    img_w = img_w.resize((w, h), PIL.Image.BILINEAR)
    img_w = np.array(img_w)
    
    mask_w = cv2.imread(path2_masks_w[j], 1)
    mask_w = cv2.resize(mask_w, (w, h), interpolation = cv2.INTER_NEAREST) # masks
    ids2assign_w.append(get_sem_id(class_names, path2_masks_w[j]))
    
    batch_imgs_w.append(img_w)
    batch_masks_w.append(mask_w)    
   
# first augmenting
_aug = augmentation_pipeline()
batch_imgs_c = _aug.augment_images(batch_imgs_c)
batch_masks_c = _aug.augment_images(batch_masks_c)

_aug2 = augmentation_pipeline()
batch_imgs_w = _aug2.augment_images(batch_imgs_w)
batch_masks_w = _aug2.augment_images(batch_masks_w)

# 2nd translating
_tug = augmentation_pipeline()
batch_imgs_c = _tug.augment_images(batch_imgs_c)
batch_masks_c = _tug.augment_images(batch_masks_c)

_tug2 = translate_pipeline()
batch_imgs_w = _tug2.augment_images(batch_imgs_w)
batch_masks_w = _tug2.augment_images(batch_masks_w)

tiled = imgviz.tile(imgs=batch_imgs_c+batch_imgs_w, border=(255, 255, 255), shape=None)# shape=(1,3)
plt.imshow(tiled)

#%
# For removing the imag and its mask if the labelled part of plant got cropped out
# during augmentation
t = []
for i in range(get_crops):
    if len(np.unique(batch_masks_c[i])) == 1: # then delete
        t.append(i)
for index in sorted(t, reverse=True):
    batch_masks_c.pop(index)
    batch_imgs_c.pop(index)
        
t = []
for i in range(get_weeds):
    if len(np.unique(batch_masks_w[i])) == 1: # then delete
        t.append(i)
for index in sorted(t, reverse=True):  
    batch_masks_w.pop(index)
    batch_imgs_w.pop(index)
    
tiled = imgviz.tile(imgs= batch_imgs_c+ batch_imgs_w, border=(255, 255, 255), shape=None)# shape=(1,3)
plt.imshow(tiled)
#%
# put crops
for i in range(len(batch_imgs_c)):
    x = batch_masks_c[i] / 255
    
    y = np.multiply(batch_imgs_c[i], x)
    
    y = y.astype(np.uint8)
    
    x = (x * ids2assign_c[i]).astype(np.uint8)
    
    z = np.where(y==0, bg_img, y)
    a = np.where(x==0, bg_mask, x)
    
    
    
    bg_img = z.astype(np.uint8)
    bg_mask = a.astype(np.uint8)
#%    
# put weeds
for i in range(len(batch_imgs_w)):
    x = batch_masks_w[i] / 255
    
    y = np.multiply(batch_imgs_w[i], x)
    
    y = y.astype(np.uint8)
    
    x = (x * ids2assign_w[i]).astype(np.uint8)
    
    z = np.where(y==0, bg_img, y)
    a = np.where(x==0, bg_mask, x)
    
    
    
    bg_img = z.astype(np.uint8)
    bg_mask = a.astype(np.uint8)

#%
rgb = gray2color(bg_mask[:,:,0], use_pallet='lip', custom_pallet=None)

plt.imshow(imgviz.tile(imgs=[bg_img, rgb], border=None, shape=(1,2)))
plt.axis('off')
#%%
temp = 10#np.random.randint(10000)

bg_img = Image.fromarray(bg_img)
rgb = Image.fromarray(rgb)
bg_mask = Image.fromarray(bg_mask)

bg_img.save(f'D:/gen_data/images/{temp}.jpg')
rgb.save(f'D:/gen_data/color_masks/{temp}.png')
bg_mask.save(f'D:/gen_data/labels/{temp}.png')
