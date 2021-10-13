# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 16:27:58 2021

@author: talha
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from skimage.morphology import convex_hull_object
mpl.rcParams['figure.dpi'] = 300
#%

def cv2_thresh_seg(image, thresh_color_rgb, apply_morph = True):
    '''
    Parameters
    ----------
    img : image to apply thresholding channel order should be RGB
    thresh_color_bgr : color value on which to apply threshold in RGB format
    apply_morph : Wheather to apply morphological operator. The default is Ture.
    Returns
    -------
    Thresholded Segmented Mask
    '''
    # if results arn't as desired try increasing or decreasing following varables
    alpha = 10
    beta = 30
    color = thresh_color_rgb # RGB Format
    hsv_color = cv2.cvtColor(color,cv2.COLOR_RGB2HSV)
    # upper bound on thresholding color
    upper = (hsv_color + np.uint8([[[alpha,0,0]]])).squeeze()
    # lower bound on thresholding color
    lower = np.array([hsv_color[0,0,0]-beta,50,50])
    lower[lower<0] = 0              # romveing -ve values
    lower = lower.astype(np.uint8)

    
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    
    if apply_morph:
        #kernel = np.ones((5,5),np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(10,10))
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        result = cv2.bitwise_and(image,image, mask= opening)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        
    else:
        result = cv2.bitwise_and(image,image, mask= mask)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        
    seg = np.ones((image.shape)) * [0, 255, 0] # RGB value of light green
    seg = np.where(result != 0, seg, result)
    
    return seg.astype(np.uint8)
#%%
dim = (512,512)
img = cv2.imread('C:/Users/talha/Desktop/Synthetic Data/images/2021-05-21_talha_bean_90_1623226243231.jpg',-1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, dim, interpolation = cv2.INTER_LINEAR)
fine_mask = cv2.imread('C:/Users/talha/Desktop/Synthetic Data/images/2021-05-21_talha_bean_90_1623226243231.png',0)
fine_mask = cv2.resize(fine_mask, dim, interpolation = cv2.INTER_NEAREST)

coarse_mask = convex_hull_object(fine_mask, connectivity=2).astype(np.uint8)

thresh_color_rgb = np.uint8([[[0,255,0]]])

op = cv2_thresh_seg(img, thresh_color_rgb, apply_morph = True)
plt.imshow(op)