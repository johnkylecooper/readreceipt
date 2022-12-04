# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 16:53:00 2022

Use pytessaract to read receipts and save to csv files to save manual labor.

@author: johnk
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

from PIL import Image
import pytesseract

# drop receipt file in folder containing this script
img = cv.imread('receipt-031222.jpg',0)

scale_percent = 500 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)

blurred = cv.GaussianBlur(resized, (7, 7), 0)

ret,th1 = cv.threshold(blurred, 200, 255,cv.THRESH_BINARY)

plt.imshow(th1, 'gray')

cv.imwrite('receipt.png', th1)

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
output = pytesseract.image_to_string(Image.open('receipt.png'))

# sort prices and names
items = []
result = output.splitlines()
for line in result:
    if ',' in line:
        items.append(line)
    
prices = []
names = []
for item in items:
    prices.append(item.split(' ')[-1])
    names.append((' ').join(item.split(' ')[:-1]))
    
# create pandas dataframe and save to csv
df = pd.DataFrame(data=np.array([names, prices]).T, columns=['product','price'])

df.to_csv('receipt.csv')