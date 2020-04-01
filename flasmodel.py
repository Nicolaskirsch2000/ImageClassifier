# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:25:06 2020

@author: Kirsch
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 15:07:18 2020

@author: Kirsch
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:33:50 2020

@author: Kirsch
"""

import pandas as pd 
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
import numpy as np
import os
from matplotlib import pyplot as plt
import cv2
import random


class ConvolutionalNetwork:
    
    #Initialise class variables
    def __init__(self, keyword1, keyword2):
        
        self.DATADIR = r"C:\Users\Kirsch\Documents\flasktest\static\uploads"

        # All the classifying possibilities
        self.CATEGORIES = [keyword1, keyword2]
            
        # The size of the images that your neural network will use
        self.IMG_SIZE = 50
        
 
        self.X = [] #features
        self.y = [] #labels
        self.training_data = []
        
        
    # Checking for all images in the data folder
    def check_img(self):
        for category in self.CATEGORIES :
            #Create path for each category
        	path = os.path.join(self.DATADIR, category)
        	for img in os.listdir(path):
                #Recuperate the images in each category
        		img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
        return img_array
         
    #Make image become pixel arrays for analysis
    def create_training_data(self):
    	for category in self.CATEGORIES :
    		path = os.path.join(self.DATADIR, category)
    		class_num = self.CATEGORIES.index(category)
    		for img in os.listdir(path):
    			try :
    				img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
    				new_array = cv2.resize(img_array, (self.IMG_SIZE, self.IMG_SIZE))
    				self.training_data.append([new_array, class_num])
    			except Exception as e:
    				pass
                
    #Shuffle the rows of the training dataset
    def shuffle(self):
        random.shuffle(self.training_data)
        return self.training_data

    #Define the features and the labels of the dataset
    def feat_and_labels(self):
        for features, label in self.training_data:
        	self.X.append(features)
        	self.y.append(label)

        self.X = np.array(self.X).reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 1)

        # Creating the files containing all the information about your model
        pickle_out = open("X.pickle", "wb")
        pickle.dump(self.X, pickle_out)
        pickle_out.close()

        pickle_out = open("y.pickle", "wb")
        pickle.dump(self.y, pickle_out)
        pickle_out.close()
        
        pickle_in = open("X.pickle", "rb")
        self.X = pickle.load(pickle_in)
        
        
        # Opening the files about data
        self.X = pickle.load(open("X.pickle", "rb"))
        self.y = pickle.load(open("y.pickle", "rb"))
        
        # normalizing data (a pixel goes from 0 to 255)
        self.X = self.X/255.0
        self.y = np.array(self.y)

        return self.y, self.X
    
    #Create the convolution neural network
    def make_model(self):
        
        # Building the model
        model = Sequential()
        # 3 convolutional layers
        model.add(Conv2D(32, (3, 3), input_shape = self.X.shape[1:]))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2)))
        
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2)))
        
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))
        
        # 2 hidden layers
        model.add(Flatten())
        model.add(Dense(128))
        model.add(Activation("relu"))
        
        model.add(Dense(128))
        model.add(Activation("relu"))
        
        # The output layer with 13 neurons, for 13 classes
        model.add(Dense(2))
        model.add(Activation("softmax"))
        
        # Compiling the model using some basic parameters
        model.compile(loss="sparse_categorical_crossentropy",
        				optimizer="adam",
        				metrics=["accuracy"])
        
        # Training the model, with 40 iterations
        # validation_split corresponds to the percentage of images used for the validation phase compared to all the images            
        history = model.fit(self.X, self.y, batch_size=32, epochs=40, validation_split=0.1)
        
        # Saving the model
        model_json = model.to_json()
        with open("model.json", "w") as json_file :
        	json_file.write(model_json)
        
        #Save model and model weights
        model.save_weights("model.h5")
        print("Saved model to disk")
        model.save(os.path.join("Models", self.CATEGORIES[0]+self.CATEGORIES[1] + '.model'))

        # Printing a graph showing the accuracy changes during the training phase
        print(history.history.keys())
        plt.figure(1)
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')

