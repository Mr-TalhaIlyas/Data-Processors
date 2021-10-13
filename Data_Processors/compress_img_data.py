# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 09:11:33 2021

@author: talha
"""

from PIL import Image, ExifTags
import cv2, glob, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import tqdm, trange
mpl.rcParams['figure.dpi'] = 300

# get the orientation of the image 
for orientation in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation]=='Orientation':
        break

def img_resizer(data_dir, dest_dir):
    imgs = os.listdir(data_dir)
    
    full_paths = [os.path.join(data_dir, c) for c in imgs] 
    new_names = []
    
    class_id = os.path.basename(dest_dir)
    for i in tqdm(full_paths, desc=f'resizing {class_id}', total=len(full_paths)):
        name = os.path.basename(i)
        
        img = Image.open(i)
        
        exif = img._getexif()
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
            
        img = img.resize((512,512))

        new_full_path = os.path.join(dest_dir, name) 
        #print(new_full_path)
        img.save(new_full_path)
    
###################
data_dir = 'H:/Data'
dest_dir = 'D:/Data_v1'

classes_found = os.listdir(data_dir)

# make dir
# for clas in classes_found:
#     os.mkdir(os.path.join(dest_dir, clas))

all_dir = os.listdir(dest_dir)
all_dest_dir = [os.path.join(dest_dir, c) for c in all_dir] 

# images word is only added for convenience because inside each classes' dir
# there were two more folders for images and labels. But we need only images
# for now.

full_paths = [os.path.join(data_dir, c+'\images') for c in classes_found] 

for full_path, final_dir in zip(full_paths, all_dest_dir):
    img_resizer(full_path, final_dir)
    