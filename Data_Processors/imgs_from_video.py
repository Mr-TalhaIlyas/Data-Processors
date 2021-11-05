# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 10:08:06 2021

@author: talha
"""

import os, glob, re
from tqdm import tqdm, trange
import matplotlib.pyplot as plt
import cv2 
import numpy as np 

vid = cv2.VideoCapture('C:/Users/talha/OneDrive/Desktop/Screen Recording (11-5-2021 9-57-09 AM).wmv')


cycle = 4500

i = 0 
j = 0
while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == False:
        break
    #frame = cv2.resize(frame, (512,512), interpolation = cv2.INTER_LINEAR)
    if i%cycle == 0:
        cv2.imwrite(f'D:/Pigs/test/cctv_pig_{j:06d}.jpg', frame)
        j+=1
    i+=1
        
    
vid.release()
cv2.destroyAllWindows()