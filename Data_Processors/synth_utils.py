# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 09:33:43 2021

@author: talha
"""

from PIL import Image, ExifTags
import cv2, glob, os, re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import tqdm, trange
from imgaug import augmenters as iaa
import imgaug as ia
mpl.rcParams['figure.dpi'] = 300

# get the orientation of the image 
for orientation in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation]=='Orientation':
        break
    
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def img_reader(path):
    
    img = Image.open(path)
        
    exif = img._getexif()
    if exif[orientation] == 3:
        img = img.rotate(180, expand=True)
    elif exif[orientation] == 6:
        img = img.rotate(270, expand=True)
    elif exif[orientation] == 8:
        img = img.rotate(90, expand=True)
    
    return img
        
def get_all_images(path):
    '''
    returns sorted list of all images in a dir and all in its sub-dir
    Parameters
    ----------
    path : path of dir/root_dir
    Returns
    -------
    filelist : list of full_paths to all the files
    '''
    filelist = []
    
    for root, dirs, files in os.walk(path, topdown=False):
    	for file in files:
            #append the file name to the list
    		filelist.append(os.path.join(root,file))
    # sort       
    filelist = sorted(filelist, key=numericalSort)
    
    return filelist

def get_sem_id(class_names, img_path):
    
    for idx in range(len(class_names)):
        if class_names[idx] in (os.path.basename(img_path)):
            return idx

def augmentation_pipeline():
    
    sometimes = lambda aug: iaa.Sometimes(0.7, aug) 
    
    seq = iaa.Sequential(
        [
        iaa.Affine(scale={"x": (0.5, 0.8), "y": (0.5, 0.8)}, order=0, backend="cv2"),
        # apply only 2 of the following
        iaa.SomeOf(3, [
        # apply only 1 of following
        # iaa.OneOf([
            sometimes(iaa.Fliplr(0.9)),
            #iaa.Affine(scale={"x": (0.35, 0.7), "y": (0.35, 0.7)}, order=0, backend="cv2"),
            sometimes(iaa.TranslateX(percent=(-0.5, 0.5), order=0, backend="cv2")),
            sometimes(iaa.Flipud(0.9)),
            sometimes(iaa.Affine(translate_percent={"x": (-0.5, 0.5), "y": (-0.5, 0.5)}, order=0, backend="cv2")),
            sometimes(iaa.Affine(rotate=(-25, 25), order=0, backend="cv2")),
            sometimes(iaa.Affine(shear=(-8, 8), order=0, backend="cv2")),
            sometimes(iaa.TranslateY(percent=(-0.5, 0.5), order=0, backend="cv2")),
            sometimes(iaa.KeepSizeByResize(
                                  iaa.Crop(percent=(0.05, 0.25), keep_size=False),
                                  interpolation='nearest')),
            ], random_order=True),
        ], random_order=True)
    
    
    _aug = seq._to_deterministic()
    
    return _aug

def translate_pipeline():
    
    min_tr = 0.2
    max_tr = 0.8
    seq = iaa.Sequential(
        [
        #iaa.SomeOf(3, [
        # apply only 1 of following
        iaa.OneOf([
            
            iaa.TranslateX(percent=(min_tr, max_tr), order=0, backend="cv2"),
            iaa.TranslateX(percent=(-max_tr, -min_tr), order=0, backend="cv2"),
            
            iaa.Affine(translate_percent={"x": (min_tr, max_tr), "y": (min_tr, max_tr)}, order=0, backend="cv2"),
            iaa.Affine(translate_percent={"x": (-max_tr, -min_tr), "y": (-max_tr, -min_tr)}, order=0, backend="cv2"),
            
            iaa.Affine(translate_percent={"x": (min_tr, max_tr), "y": (-max_tr, -min_tr)}, order=0, backend="cv2"),
            iaa.Affine(translate_percent={"x": (-max_tr, -min_tr), "y": (min_tr, max_tr)}, order=0, backend="cv2"),
            
            iaa.TranslateY(percent=(min_tr, max_tr), order=0, backend="cv2"),
            iaa.TranslateY(percent=(-max_tr, -min_tr), order=0, backend="cv2")
            ]),
        ], random_order=True)
    
    
    _aug = seq._to_deterministic()
    
    return _aug