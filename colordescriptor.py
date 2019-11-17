import numpy as np
import cv2
# from skimage.feature import hog
# from skimage import exposure

class ColorDescriptor:
    def __init__(self, bins):
        self.bins=bins
        
    def describe(self, image):
        # convert image to HSV
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []   # initialize features
        
        # grab dimensions and compute center of image
        (h,w) = image.shape[:2]
        (cX, cY) = (int(w*0.5), int(h*0.5))
        
        ### Region based color descriptor
        
        # divide image into 4 rectangles 
        segments = [(0,cX,0,cY), (cX,w,0,cY), (cX,w,cY,h),
                    (0,cX,cY,h)]
        # elliptical mask at center of image
        (axesX, axesY) = (int(w*0.75)//2, int(h*0.75)//2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX,cY), (axesX, axesY), 0,0,360,255,-1)
        
        # loop over segment
        for (startX, endX, startY, endY) in segments:
            # construct mask for each corner of image,
            # subtracting the elliptical center
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)
            
            # extract a color histogram from the image
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
            
        # extract color histogram from elliptical region
        hist = self.histogram(image, ellipMask)
        features.extend(hist)
        
        return features

    # def describe_hog(self, image):
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     hog_features = []   # initialize features
    #     fd, hog_image = hog(img, orientations=9, pixels_per_cell=(8, 8),cells_per_block=(2, 2), visualize=True, multichannel=True)
    #     hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
    #     return hog_image_rescaled

    
    def histogram(self, image, mask):
        hist = cv2.calcHist([image], [0,1,2], mask, self.bins,
                            [0,180,0,256,0,256])
        
        hist = cv2.normalize(hist, hist).flatten()
        
        return hist