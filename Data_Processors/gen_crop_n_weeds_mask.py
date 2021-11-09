# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 09:25:27 2021

@author: talha
"""

import os, glob, re
from tqdm import tqdm, trange
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
import cv2 
import numpy as np 
import json
from cv2_thresh_seg import cv2_thresh_seg
from morphology import get_sem_bdr

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

# pallet for crop and weeds
pallet_cnw = np.array([[[0, 0, 0],
                        [255, 0, 0],
                        [255, 255, 0]]], np.uint8) / 255

img_dir = 'D:/B/bean_data/final/images/'
mask_dir = 'D:/B/bean_data/final/masks_full/'

op_dir = 'D:/B/bean_data/final/overlayed/'

# path to json files
img_paths = glob.glob(os.path.join(img_dir, '*.jpg')) 
mask_paths = glob.glob(os.path.join(mask_dir, '*.png')) 
# sort the file paths
img_paths = sorted(img_paths, key=numericalSort)
mask_paths = sorted(mask_paths, key=numericalSort)

error = []
for i in trange(len(img_paths)):
    
    x = cv2.imread(mask_paths[i], 0)
    y = cv2.imread(img_paths[i])
    y = cv2.cvtColor(y,cv2.COLOR_BGR2RGB) 
    '''
    Use only 1 func at once:
    Func 1 for overlaying masks and images.
    Func 2 for combining weeds and crop masks into one.
    '''
    ###############################_Function 1_################################
    x = cv2.resize(x, (512,512), interpolation = cv2.INTER_NEAREST)
    y = cv2.resize(y, (512,512), interpolation = cv2.INTER_LINEAR)

    op = get_sem_bdr(x, y, blend=True, custom_pallet=pallet_cnw) 
    
    name = os.path.basename(mask_paths[i])
    op = cv2.cvtColor(op,cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'{op_dir}/{name}', op)
    ###############################_Function 2_################################
    # # generate inv mask to remove the plant from image
    # a = 1 - x
    # # replacte mask to RGB channels
    # a = cv2.merge((a,a,a))
    # try:
    #     z = np.multiply(y, a)
    #     # define whihc color to remove from image
    #     thresh_color_rgb = np.uint8([[[0,255,0]]]) 
    
    #     op = cv2_thresh_seg(z, thresh_color_rgb)
    #     op = np.argmax(op, axis=2) # to get 1 channel wiht 1's at weed locations
    #     #plt.imshow(op)
    #     final = np.add(op*2, x)
    #     #plt.imshow(final)
    
    #     name = os.path.basename(mask_paths[i])
    #     cv2.imwrite(f'{op_dir}/{name}', final)
    # except ValueError:
    #     error.append(os.path.basename(img_paths[i]))