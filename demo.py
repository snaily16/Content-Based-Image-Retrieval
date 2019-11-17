import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo



app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/DemoIMGs'

mongo = PyMongo(app)

@app.route('/')
def index():
	data = mongo.db.myImages.find({"filename" : "dataset/138.jpg"})
	#image_name = data["filename"]
	l=[]
	for d in data:
		l.append(d)
	return render_template('index.html', data=str(l))

if __name__ == '__main__':  
    app.run(debug = True) 