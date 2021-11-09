# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 12:49:26 2021

@author: talha
"""

import os, glob, re, cv2, shutil
from tqdm import tqdm, trange
import numpy as np 
from sklearn.model_selection import train_test_split

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

img_dir = 'D:/B/bean_data/final/images/'
mask_dir = 'D:/B/bean_data/final/masks_full/'

op_dir = 'D:/B/bean_data/final/DATA_FOLDER/'

# path to json files
img_paths = glob.glob(os.path.join(img_dir, '*.jpg')) 
mask_paths = glob.glob(os.path.join(mask_dir, '*.png')) 
# sort the file paths
img_paths = sorted(img_paths, key=numericalSort)
mask_paths = sorted(mask_paths, key=numericalSort)

test_data = 0.23
val_data = 0.15

x_train_val, x_test, y_train_val, y_test = train_test_split(img_paths, mask_paths,
                                                            test_size=test_data, random_state=42)

x_train, x_val, y_train, y_val = train_test_split(x_train_val, y_train_val,
                                                            test_size=val_data, random_state=42)

x = len(img_paths)
print(f'{30*"*"} \n Total {x} images found. \n\
      Train Data = {len(x_train)} \n\
      Test Data = {len(x_test)} \n\
      Val Data = {len(x_val)}\n{30*"*"}')
#%
img_data = [x_train, x_test, x_val]
label_data = [y_train, y_test, y_val]

sub_dir = ['train', 'test', 'val']

for i in range(len(sub_dir)):
    im_path = os.path.join(op_dir, sub_dir[i] + '/images/')
    ms_path = os.path.join(op_dir, sub_dir[i] + '/masks/')
    for j,k in tqdm(zip(img_data[i],label_data[i]), desc=f'Creating {sub_dir[i]} set', total=len(img_data[i])):
        shutil.copy2(j, im_path)
        shutil.copy2(k, ms_path)
        
