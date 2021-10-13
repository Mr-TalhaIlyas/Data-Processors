# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 08:17:09 2021

@author: talha
"""

import cv2, glob, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

'''
The order of names in the following 2 lists should be same.
'''
# korean and encoded name that needs to be replaced (in order*)
k_name = ['미국개기장', '기장', '녹두', '들깨', '땅콩', '수수', '옥수수', '조', 
          '참깨', '콩', '팥', '바랭이', '강피', '새포아풀', '왕바랭이', '강아지풀',
          '나도논피', '돌피', '도', '정면', '상부', '±âÀå', '³ìµÎ', 'µé±ú', '¶¥Äá',
          '¼ö¼ö', '¿Á¼ö¼ö', 'Á¶', 'Âü±ú', 'Äá', 'ÆÏ']

# english names that will replace kor or enc name (in order*)
e_name = ['fall_panicum', 'proso_millet', 'green_gram', 'perilla', 'peanut', 
          'great_millet', 'corn', 'foxtail_millet', 'sesame', 'bean', 'red_bean',
          'southern_crabgrass', 'rice_cockspur', 'poa_annua', 'indian_goosegrass',
          'green_foxtail', 'e_oryzoides', 'cockspur_grass', 'degree', 'front', 
          'top', 'proso_millet', 'green_gram', 'perilla', 'peanut', 'great_millet',
          'corn', 'foxtail_millet', 'sesame', 'bean', 'red_bean',]


ddir = 'C:/Users/talha/OneDrive/Desktop/temp/A'

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
    