# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:56:45 2020

@author: Kirsch
"""

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flaseco import ImageSearch
from flasmodel import ConvolutionalNetwork
from flastyp import TestYourPic

UPLOAD_FOLDER = r"static\uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jfif'}



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    #Create the names of the two possibilities the two possibilities 
    name = request.form.get("rName")
    name1 = request.form.get("rName1")
    numpic = request.form.get("numpic")
    modelexist = not os.path.exists(os.path.join("Models", name+name1+'.model'))
    
    if  modelexist :
        #Create the first image databases
        image1 = ImageSearch(name, numpic)
        image1.pic_direc()
        image1.new_webpage()
        image1.scroll()
        image1.takepic()
        image1.closebrowser()
    
        #Create the second image database
        image2 = ImageSearch(name1, numpic)
        image2.pic_direc()
        image2.new_webpage()
        image2.scroll()
        image2.takepic()
        image2.closebrowser()
    
        #Create and train the network
        network = ConvolutionalNetwork(name,name1 )
        network.create_training_data()
        network.shuffle()
        network.feat_and_labels()
        network.make_model()
    
    if request.method == 'POST':  
        #Recuperate the uploaded file informations
        f = request.files['file'] 
        
        #Save the image 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename)) 
        
        #Create the new filepath
        filepath = 'uploads/' + f.filename
        
        #Check what is this pick
        test = TestYourPic(name,name1, f.filename)
        result =  test.test()
        
    processed_name = name.upper()
    processed_name1 = name1.upper()
    return render_template("bienvenue.html" , message = processed_name, 
                           message1 = processed_name1, 
                           user = filepath, result = result,
                           name = f.filename)

@app.route("/next", methods=['GET', 'POST'])
def uploadingpage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    return render_template('upload.html')

@app.route("/success", methods=['POST', 'GET'])
def success():  
   if request.method == 'POST':  
        #Recuperate the uploaded file informations
        f = request.files['file'] 
        
        #Save the image 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename)) 
        
        #Create the new filepath
        filepath = 'uploads/' + f.filename
        
        #Check what is this pick
        test = TestYourPic(name,name1, f.filename)
        result =  test.test()
        return render_template("image.html", name = f.filename, user = filepath, result = result)  


#Run the webapp
if __name__ == '__main__':
    app.run()