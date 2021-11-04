# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:06:56 2021

@author: talha
"""

import os, glob, re, io, base64
from tqdm import tqdm, trange
from PIL import Image
import matplotlib.pyplot as plt
import cv2 
import numpy as np 
import json
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def str2img(imgdata):
    '''
    For reading images from a json/str file
    Parameters
    ----------
    imgdata : image data in str format e.g. 'iVBORw0KG...'
    
    Returns
    -------
    img : a PIL image object
    '''
    img_bytes = base64.b64decode(imgdata)
    img_io = io.BytesIO(img_bytes)
    img = Image.open(img_io)
    return img

def img2str(img):
    '''
    For writing image data in a json/str format
    Parameters
    ----------
    img : a PIL image object

    Returns
    -------
    string : image data in str format e.g. 'iVBORw0KG...'
    '''
    output = io.BytesIO()
    img.save(output, format="png")
    image_as_string = output.getvalue()
    converted_string = base64.b64encode(image_as_string)
    string = converted_string.decode('utf-8')
    return string

direc = 'D:/Pigs/sequence_image/8/'


base_file = glob.glob(os.path.join(direc, '*.json'))[0]

with open(base_file) as json_file:
    j_file = json.load(json_file)
    
imgs = glob.glob(os.path.join(direc, '*.png')) 

for i in range(len(imgs)):
    img = Image.open(imgs[i])
    name = os.path.basename(imgs[i])[:-4]
    string = img2str(img)
    j_file['imageData'] = string
    
    with open(f'{direc}/{name}.json', 'w') as fp:
        json.dump(j_file, fp)


