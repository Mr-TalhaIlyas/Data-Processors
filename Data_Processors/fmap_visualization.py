# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:01:09 2022

@author: talha
"""

import tensorflow as tf
from tensorflow.keras.models import Model

model = tf.keras.applications.ResNet50(include_top = False, weights = 'imagenet',
                                               input_shape = (256, 256, 3),
                                               pooling = 'avg', classes = 1)


model = Model(inputs=model.input, outputs=model.output)  
activation_model = model
#%% Visualizations
'''
Start and import the model for plotting the f_maps and get the names of all the layers from the model
(see the names of the layers from the pydot plot or from variable explorer). Then provide the index of 
layer you wanna claculate f_maps of.
'''
import cv2
import numpy as np
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
layer_outputs = [layer.output for layer in model.layers[1:]]#Dont' include the input layer in your output fetch layers i.e. start from (1:)
activation_model = Model(inputs=model.input, outputs=layer_outputs) # Creates a model that will return these outputs, given the model input
layer_names = []
for layer in model.layers[1:]:
    layer_names.append(layer.name) # Names of the layers, so you can have them as part of your plot
img1 = cv2.imread('C:/Users/talha/Desktop/car.png') 
img1 = cv2.resize(img1, (256, 256))
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img1 = img1[np.newaxis,:,:,:]
activations = activation_model.predict(img1)
plt.imshow(img1.squeeze())
#%%   Plot activation for Conv layers
'''
Get the index number of layer you wanna see from the variable explorer.
'''
layer_index = 36
layer_activation = activations[layer_index]
print('Layer name is =', layer_names[layer_index])
print('Feature Maps shape is =', layer_activation.shape)

images_per_row = 8
n_features = layer_activation.shape[-1]//8 # Number of features in the feature map
size = layer_activation.shape[1] #The feature map has shape (1, size, size, n_features).
n_cols = n_features // images_per_row # Tiles the activation channels in this matrix
display_grid = np.zeros((size * n_cols, images_per_row * size))

for col in range(n_cols): # Tiles each filter into a big horizontal grid
        for row in range(images_per_row):
            channel_image = layer_activation[0,:, :,col * images_per_row + row]
            channel_image -= channel_image.mean() # Post-processes the feature to make it visually palatable
            channel_image /= channel_image.std()
            channel_image *= 64
            channel_image += 128
            channel_image = np.clip(channel_image, 0, 255).astype('uint8')
            display_grid[col * size : (col + 1) * size, row * size : (row + 1) * size] = channel_image # Displays the grid
scale = 1. / size
plt.figure(figsize=(scale * display_grid.shape[1],
                    scale * display_grid.shape[0]))
#plt.title(layer_names[layer_index])
plt.grid(False)
plt.imshow(display_grid, aspect='auto', cmap='viridis') # viridis, seismic, gray, ocean, CMRmap, RdYlBu, rainbow, jet

#layer_activation = ReLu(layer_activation)
#plt.imshow(layer_activation[0,:,:,8], cmap='jet')
plt.axis('off')
#%%    Plot activation for FC layers

layer_index = 11
layer_activation = activations[layer_index]
layer_reduced = layer_activation.squeeze()
layer_reduced = layer_reduced[np.newaxis,:]
layer_reduced = layer_reduced.T
plt.figure()
plt.axis('off')
plt.imshow(layer_reduced)