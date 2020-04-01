# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:48:43 2020

@author: Kirsch
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:35:12 2020

@author: Kirsch
"""

#Importing packages
from selenium import webdriver
import urllib   
import time 
import os



#Constant variable for time between scrolls
SCROLL_PAUSE_TIME = 1

class ImageSearch:
    
    def __init__(self, keyword, numpic): 
        self.keyword = keyword
          # Parent Directory path 
        parent_dir = r"static\uploads"
        #Create the path where the pictures will be stored 
        self.path = os.path.join(parent_dir, keyword)
        self.url = 'https://www.ecosia.org/images?q=' + keyword
        self.numpic = int(numpic)
    #Create the new directory
    def pic_direc(self): 
       
        if not os.path.exists(self.path):
        #Create the directory
            os.mkdir(self.path)
        return self.path
                
    #Create the webdriver and open the searched webpage
    def new_webpage(self):
        self.driver = webdriver.Chrome(r"static\chromedriver.exe")
        
        self.driver.get(self.url)
    
    #Scroll down to load all the pictures
    def scroll(self):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
    
        while True:
        # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
    
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
           
    #Download the picture        
    def takepic(self):
    
        src = [None]*300
        for i in range (1, self.numpic):
            img = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div/a[' + str(i) + ']/img')
            print(self.keyword)
            
            src[i] = img.get_attribute('src')
            if src[i] == None:
                i +=1
            else: 
                # download the image
                urllib.request.urlretrieve(src[i], self.path + '/' + self.keyword + str(i) + '.png')
            
                    
    def closebrowser(self):
        self.driver.quit()
