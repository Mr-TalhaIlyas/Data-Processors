# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 17:03:41 2021

@author: talha
"""

import os, shutil
from tqdm import tqdm

path2copy = "D:/Binary_Seg_Data_C/temp/"
path2match = "D:/Binary_Seg_Data_C/temp2/" 
path2paste = "D:/Binary_Seg_Data_C/temp3/" 
#we shall store all the file names in this list
all_filelist = []


for root, dirs, files in os.walk(path2copy, topdown=False):
	for file in files:
        #append the file name to the list
		all_filelist.append(os.path.join(root,file))
        

file_names = os.listdir(path2match)
for i in range(len(file_names)):
    file_names[i] = file_names[i].replace('.JPG','')

all_file_names = [os.path.basename(c) for c in all_filelist]
for i in range(len(all_file_names)):
    all_file_names[i] = all_file_names[i].replace('.png','')

ids = []

for j in range(len(file_names)):
    try:
        x = all_file_names.index(file_names[j])
        ids.append(x)
    except ValueError:
        print('Error')
        pass
    
#%%    

for k in tqdm(ids, desc='Moving', total=len(ids)):
    shutil.copy2(all_filelist[k], path2paste)
#%%
def non_match_elements(list_a, list_b):
    j = 0
    non_match_id = []
    for i in list_a:
        j = j + 1
        if i not in list_b:
            non_match_id.append(j)
    return non_match_id


ids = non_match_elements(all_file_names, file_names)

# for f in tqdm(filelist, desc='Moving Data', total=len(filelist)):
#     shutil.copy2(f, dest_dir)
    