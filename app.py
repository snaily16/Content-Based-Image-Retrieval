import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
import numpy as np
from colordescriptor import ColorDescriptor
import gridfs as gfs
from searcher_mdb import Searcher
import cv2


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/FlickrDB'
mongo = PyMongo(app)

fs = gfs.GridFS(mongo.db)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
	# check if a valid image was uploaded
	if request.method == 'POST':
		if 'file' not in request.files:
			return redirect(request.url)

		file = request.files['file']
		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			return render_template(
				'upload.html', results = search(file.filename), filename=file.filename
				)
	return render_template('upload.html')

def search(query):
	#print(query)
	cd = ColorDescriptor((8, 12, 3))
	query = cv2.imread(query)
	query = cv2.resize(query,(416,416))
	features = cd.describe(query)
	searcher = Searcher()
	results = searcher.search(features)

	#cv2.imshow("Query", query)
	# loop over the results
	for (score, resultID) in results:
		# load the result image and display it
		#print(resultID)
		img = mongo.db.myImages.find({'filename': resultID},{"_id": 0 , "name": 0, "filename": 0})
		l=[]
		for x in img:
			#print(x)
			x = x['images'][0]

			#print('hey')
			#print(x)
			fout = fs.get(x['imageID'])

			im = np.frombuffer(fout.read(), dtype=np.uint8)
			im = np.reshape(im, x['shape'])
		# cv2.imshow("Result", im)
		# cv2.waitKey(0)

	return results

if __name__ == '__main__':  
    app.run(debug = True) 