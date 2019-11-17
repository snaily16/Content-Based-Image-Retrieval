# import the necessary packages
from pymongo import MongoClient
import gridfs as gfs
import numpy as np
import csv

class Searcher:
	def __init__(self):
		# store our index path
		#self.indexPath = indexPath
		pass

	def search(self, queryFeatures, limit = 25):
		# initialize our dictionary of results
		results = {}

		client = MongoClient('localhost', 27017)
		db = client['FlickrDB']
		coll = db['myImages']

		fs = gfs.GridFS(db)
		q = coll.find({})
		for r in q:
			#print(row)
			rimg = r["images"]
			image_name = r["filename"]

			for ri in rimg:
				reader = ri["feature"]

				features = [float(x) for x in reader]
				d = self.chi2_distance(features, queryFeatures)
				#print(d)
				results[image_name] = d

		# sort our results, so that the smaller distances (i.e. the
		# more relevant images are at the front of the list)
		results = sorted([(v, k) for (k, v) in results.items()])

		# return our (limited) results
		return results[:limit]
    
	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])

		# return the chi-squared distance
		return d