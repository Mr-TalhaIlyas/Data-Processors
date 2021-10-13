# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 10:40:53 2021

@author: talha
"""

# from google_trans_new import google_translator  
# translator = google_translator()  
# translate_text = translator.translate('Hola mundo!', lang_src='es', lang_tgt='en')  
# print(translate_text)

import cv2, glob, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import tqdm, trange
mpl.rcParams['figure.dpi'] = 300

data_dir = 'H:/Data'
#dest_dir = 'D:/Data_v1'

k_name = ['미국개기장', '기장', '녹두', '들깨', '땅콩', '수수', '옥수수', '조', 
          '참깨', '콩', '팥', '바랭이', '강피', '새포아풀', '왕바랭이', '강아지풀',
          '나도논피', '돌피', '도', '정면', '상부', '±âÀå', '³ìµÎ', 'µé±ú', '¶¥Äá',
          '¼ö¼ö', '¿Á¼ö¼ö', 'Á¶', 'Âü±ú', 'Äá', 'ÆÏ']

e_name = ['fall_panicum', 'proso_millet', 'green_gram', 'perilla', 'peanut', 
          'great_millet', 'corn', 'foxtail_millet', 'sesame', 'bean', 'red_bean',
          'southern_crabgrass', 'rice_cockspur', 'poa_annua', 'indian_goosegrass',
          'green_foxtail', 'e_oryzoides', 'cockspur_grass', 'degree', 'front', 
          'top', 'proso_millet', 'green_gram', 'perilla', 'peanut', 'great_millet',
          'corn', 'foxtail_millet', 'sesame', 'bean', 'red_bean',]

def file_renamer(data_dir):
    imgs = os.listdir(data_dir)
    
    full_paths = [os.path.join(data_dir, c) for c in imgs] 
    new_names = []
    
    for i in full_paths:
        name = os.path.basename(i)
        for j in range(len(k_name)):        
            temp = name.replace(k_name[j], e_name[j])
            name = temp
            
        #print(name)
        new_names.append(name)
        
    new_full_paths = [os.path.join(data_dir, c) for c in new_names] 
    
    [os.rename(full_paths[c], new_full_paths[c]) for c in range(len(full_paths))]
    
    
    
classes_found = os.listdir(data_dir)

# images word is only added for convenience because inside each classes' dir
# there were two more folders for images and labels. But we need only images
# for now.

full_paths = [os.path.join(data_dir, c+'\images') for c in classes_found] 

for full_path in tqdm(full_paths, desc='Renaming', total=len(full_paths)):
    
    file_renamer(full_path)
    
    # temp = os.listdir(full_path)
    # #print(len(temp))
    # img_paths = [os.path.join(full_path, img) for img in temp]
    
    # for i in img_pahts:
        
    #     name = os.path.basename(i)
    #     img = cv2.imread(i)


