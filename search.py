
# import the necessary packages
from colordescriptor import ColorDescriptor
#from searcher import Searcher
from pymongo import MongoClient
import gridfs as gfs
from searcher_mdb import Searcher
import numpy as np
import argparse
import cv2

client = MongoClient('localhost', 27017)
db = client['FlickrDB']
coll = db['myImages']

fs = gfs.GridFS(db)

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
query = cv2.imread(args["query"])
#query = cv2.resize(query,(416,416))
#cv2.imwrite('static', query) 
features = cd.describe(query)

# perform the search
searcher = Searcher(args["index"])
results = searcher.search(features)

# display the query
cv2.imshow("Query", query)

# loop over the results
for (score, resultID) in results:
	# load the result image and display it
	print(resultID)
	img = coll.find_one({'filename': resultID})['images'][0]
	fout = fs.get(img['imageID'])

	im = np.frombuffer(fout.read(), dtype=np.uint8)
	im = np.reshape(im, img['shape'])
	#print(im)
	cv2.imshow("Result", im)
	cv2.waitKey(0)
