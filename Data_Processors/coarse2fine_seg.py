# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 11:38:59 2021

@author: talha
"""

import cv2, glob, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from skimage.morphology import convex_hull_object
mpl.rcParams['figure.dpi'] = 300

dim = (512,512)
img = cv2.imread('C:/Users/talha/Desktop/Synthetic Data/images/2021-05-21_talha_bean_90_1623226243231.jpg',-1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, dim, interpolation = cv2.INTER_LINEAR)
fine_mask = cv2.imread('C:/Users/talha/Desktop/Synthetic Data/images/2021-05-21_talha_bean_90_1623226243231.png',0)
fine_mask = cv2.resize(fine_mask, dim, interpolation = cv2.INTER_NEAREST)

coarse_mask = convex_hull_object(fine_mask, connectivity=2).astype(np.uint8)
#%%
def water(img, mask):
    '''
    Parameters
    ----------
    img : 3D array, RGB iamge [H W 3]
    mask : 2D array, semantic/binary segmentaion mask [H W]

    Returns
    -------
    img : RGB image wiht overlayd boundry instances
    new : instacnes boundaries
    '''
    img = (img).astype(np.uint8)
    mask = (mask).astype(np.uint8)
    original_image = np.copy(img)
    
    # apply threshold to converto sem-mask to binary mask
    ret, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # so that BG pixel have 0 value and FG will have 255 value
    thresh = 255 - thresh
    
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    # Normalize the distance image for range = {0.0, 1.0}
    # so we can visualize and threshold it 
    dist_transform = cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)
    _, sure_fg = cv2.threshold(dist_transform, 0.4, 1.0, cv2.THRESH_BINARY)
    #ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    
    # remove bg form the image so that water shed will only focus on cells
    img[thresh==0]=1
    
    markers = markers.astype('int32')
    markers = cv2.watershed(img, markers)
    # draw boundaries on real iamge
    original_image[markers == -1] = [255,0,0]
    # draw boundary on empty convas
    new = np.zeros(img.shape)
    new[markers == -1] = [255, 255, 255]
    new = (new).astype(np.uint8)
    new = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
    new = (new/255).astype(np.uint8)
    return original_image, new

#%%
x, y = water(img, thresh)

plt.imshow(x)