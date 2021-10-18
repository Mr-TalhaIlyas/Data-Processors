# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 10:27:52 2021

@author: talha
"""
from PIL import Image, ExifTags
import os
from tqdm import tqdm
# get the orientation of the image 
for orientation in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation]=='Orientation':
        break

def remove_exif_data(data_dir, dest_dir):
    imgs = os.listdir(data_dir)
    
    full_paths = [os.path.join(data_dir, c) for c in imgs] 
    new_names = []
    
    class_id = os.path.basename(dest_dir)
    for i in tqdm(full_paths, desc=f'Removing Exif_data {class_id}', total=len(full_paths)):
        name = os.path.basename(i)
        
        img = Image.open(i)
        
        exif = img._getexif()
        if exif[orientation] == 3:
            img = img.rotate(180, expand=False)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=False)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=False)
            
        new_full_path = os.path.join(dest_dir, name) 
        #print(new_full_path)
        img.save(new_full_path)
        
        
data_dir = "D:/binary_seg_data/images/crops_90/"
dest_dir = 'D:/binary_seg_data/images/crops_90/'


remove_exif_data(data_dir, dest_dir)
