# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 01:10:16 2020

@author: Kirsch
"""

import cv2
import tensorflow as tf
import os 

class TestYourPic:
    
    def __init__(self, keyword1, keyword2, picname):
        
        self.IMG_SIZE = 50
        #Class that can be predicted
        self.CATEGORIES = [keyword1, keyword2]
        #Directory for testing pictures
        self.parent_path = r'C:\Users\Kirsch\Documents\flasktest\static\uploads'
        self.picname = picname

    #Format the picture to the right size        
    def prepare(self):
        img_array = cv2.imread(self.file, cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_array, (self.IMG_SIZE, self.IMG_SIZE))
        return new_array.reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 1)
        
    #Classify the picture
    def test(self):
       model = tf.keras.models.load_model(os.path.join("Models", self.CATEGORIES[0]+self.CATEGORIES[1] + '.model'))
       self.file = os.path.join(self.parent_path,self.picname)
       if os.path.exists(self.file): 
           image = self.prepare()
           #Make the prediction
           prediction = model.predict([image])
           prediction = list(prediction[0])
           return self.CATEGORIES[prediction.index(max(prediction))]
       else :
           return 'wola ca existe pas fils de mais'
        