import os
import sys

import cv2
import numpy as np

#Input file 
input_f = 'letter.data' 

img_resize_factor = 14
start = 6
end = -1
height, width = 18, 9


with open(input_file, 'r') as f:
    for l in f.readlines():
        
        data = np.array([255 * float(x) for x in line.split('\t')[start:end]])

        # Reshape the data into a 2D image
        img = np.reshape(data, (height, width))
        
        img_scaled = cv2.resize(img, None, fx=img_resize_factor, fy=img_resize_factor)

        cv2.imshow('Image', img_scaled)

        # Check if the user pressed the Esc key
        c = cv2.waitKey()
        if c == 27:
            break
