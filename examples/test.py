# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 15:56:31 2017

@author: Lachlan
"""

import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

img=mpimg.imread('signs_vehicles_xygrad.jpg')
red = np.copy(img)
red[:,:,1:] = 0
print('red', red)
green = np.copy(img)
green[:,:,0:3:2] = 0
print('green', green)
blue = np.copy(img)
blue[:,:,:2] = 0
print('blue', blue)
black = np.zeros_like(img)
white = np.zeros_like(img) + 255

print(img.shape)
fig = plt.figure()
a = plt.imshow(img)
fig2 = plt.figure()
fig2.add_subplot(1,3,1)
plt.imshow(red)
fig2.add_subplot(1,3,2)
plt.imshow(green)
fig2.add_subplot(1,3,3)
plt.imshow(blue)
fig3 = plt.figure()
fig3.add_subplot(1,2,1)
plt.imshow(white)
fig3.add_subplot(1,2,2)
plt.imshow(black)
