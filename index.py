from colordescriptor import ColorDescriptor
from pymongo import MongoClient
import gridfs as gfs
import argparse
import glob
import cv2

client = MongoClient('localhost', 27017)
db = client['FlickrDB']
coll = db['myImages']

fs = gfs.GridFS(db)
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images to be indexed")
args = vars(ap.parse_args())
 
# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
	# extract the image ID (i.e. the unique filename) from the image
	# path and load the image itself
	imageName = imagePath[imagePath.rfind("/") + 1:]
	image = cv2.imread(imagePath)

	# describe the image
	features = cd.describe(image)
	features = [str(f) for f in features] 
	imgString = image.tostring()

	imageID = fs.put(imgString, encoding='utf-8')
    
    # create our image meta data
	meta = {
		'name': 'myImageDatasets',
        'filename': imagePath,
		'images': [
        {
            'imageID': imageID,
            'shape' : image.shape,
            'dtype' : str(image.dtype),
            'feature':features
        }
        ]
    }
            
	coll.insert_one(meta)