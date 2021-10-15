# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:00:54 2021

@author: talha

Copy all the file inside a dir and it's sub-dir into a new dir.
"""


import os, shutil
from tqdm import tqdm

path = "C:/Users/talha/Downloads/Orig Seg/Orig_Seg"
dest_dir = "D:/Binary_Seg_Data_C/images/" 
#we shall store all the file names in this list
filelist = []

for root, dirs, files in os.walk(path, topdown=False):
	for file in files:
        #append the file name to the list
		filelist.append(os.path.join(root,file))
        
for f in tqdm(filelist, desc='Moving Data', total=len(filelist)):
    shutil.copy2(f, dest_dir)
    