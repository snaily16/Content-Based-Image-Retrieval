import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

path ='Flickr8k_Dataset/Flicker8k_Dataset'
new_path = 'flickr_dataset'

i = 0

for file in os.scandir(path):
	os.rename(file.path, os.path.join(path, '{}.jpg'.format(i)))
	i = i+1

if not os.path.exists(new_path):
	os.makedirs(new_path)

pic=0
for i in os.scandir(path):
	img=cv2.imread(i.path)
	resized_image = cv2.resize(img,(416,416))
	cv2.imwrite(new_path+'/'+str(pic)+'.jpg', resized_image)
	pic=pic+1