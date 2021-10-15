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
k_name = ['미국개기장','왕바랭이','옥수수', '기장', '녹두', '들깨', '땅콩', '수수', '조', 
          '참깨', '콩', '팥', '바랭이', '강피', '새포아풀', '강아지풀',
          '나도논피', '돌피', '도', '정면', '상부', '측면', '±âÀå', '³ìµÎ', 'µé±ú', '¶¥Äá',
          '¼ö¼ö', '¿Á¼ö¼ö', 'Á¶', 'Âü±ú', 'Äá', 'ÆÏ', 
          '중⃝중⃝_', '쵒쵒_']

# english names that will replace kor or enc name (in order*)
e_name = ['fall_panicum', 'indian_goosegrass', 'corn', 'proso_millet', 'green_gram', 'perilla', 'peanut', 
          'great_millet', 'foxtail_millet', 'sesame', 'bean', 'red_bean',
          'southern_crabgrass', 'rice_cockspur', 'poa_annua', 
          'green_foxtail', 'e_oryzoides', 'cockspur_grass', 'degree', 'front', 
          'top', 'side', 'proso_millet', 'green_gram', 'perilla', 'peanut', 'great_millet',
          'corn', 'foxtail_millet', 'sesame', 'bean', 'red_bean', '', '']


# if one name has problem
# k_name = ['옥great_millet']
# e_name = ['corn']

ddir = 'H:/Data/corn/images'

def file_renamer(data_dir):
    imgs = os.listdir(data_dir)
    
    full_paths = [os.path.join(data_dir, c) for c in imgs] 
    new_names = []
    
    for i in full_paths:
        name = os.path.basename(i)
        
        '''Method 1 (be mindful of file extensions)'''
        # name = name.replace('.png', '')
        # temp = name.split('_')
        # if len(temp) !=1:
        #     try:
        #         int(temp[-1].replace(')', ''))
        #     except ValueError:
        #         temp.pop() # delete last entry
        # name = '_'.join(temp) + '.png'
        #***********************************
        '''Method 2'''
        for j in range(len(k_name)):        
            temp = name.replace(k_name[j], e_name[j])
            name = temp
        #***********************************
        '''Method 3 (be mindful of file extensions)'''
        # name = name.replace('.JPG', '')
        # name = name.replace('.jpg', '')
        # temp = name.split('_')
        # for i in reversed(temp):
        #     try:
        #         int(i)
        #         break
        #     except:
        #         temp.pop()
        # name = '_'.join(temp) + '.JPG'
        #***********************************
        
        #print(name)
        new_names.append(name)
        
    new_full_paths = [os.path.join(data_dir, c) for c in new_names] 
    [os.rename(full_paths[c], new_full_paths[c]) for c in range(len(full_paths))]
    
    
file_renamer(ddir)
