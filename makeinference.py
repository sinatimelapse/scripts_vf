import time
import sys
import os
import cv2
import numpy as np
import pickle as cPickle
import torch 
import json  
import pandas as pd


start_time = time.time()

SHAPE = (20, 20)

#Function for reading files from the command line 
def read_files(directory):
   print("Reading files...")
   images_list = list()
   files = os.listdir(directory)
   for filename in files:
      images_list.append(filename)
   return images_list 
   
#Function for extracting features to classify dark images
def extract_feature(image_file):
   img = cv2.imread(image_file)
   img = cv2.resize(img, SHAPE, interpolation = cv2.INTER_CUBIC)
   img = img.flatten()
   #img = img/np.mean(img)
   return img



#Function for extracting features to classify edge images
def extract_feature_edge(image_file):
   img = cv2.imread(image_file,0)
   img = cv2.resize(img, SHAPE, interpolation = cv2.INTER_CUBIC)
   img = cv2.Canny(img,100,200)
   img = img.flatten()
   #img = img/np.mean(img)
   return img



if __name__ == "__main__":
   if len(sys.argv) < 2:
      print ("Usage: python extract_features.py [image_folder]")
      exit()

   # Directory containing subfolders with images in them.
   directory = sys.argv[1]

   # generating two numpy arrays for features and labels
   images= read_files(directory)
   

####################################################################
print("The first classification has started ")    
#load dark classification model
with open('svm_model.pkl' , 'rb') as f :
    model = cPickle.load(f)

cpt=0
for i in images :
   
   path = './tiled/%s'%i
   img = extract_feature(path) 
   img = img.reshape(1, -1)
   label=model.predict(img)
   print(i,'',label) 
   
   
   if (label =="night") :
      cpt=cpt+1
      os.remove(path)


print("%d Deleted images !!!"%cpt)

##################################################################



print("The second classification classification has started ")    
#load svm_model_edge classification model
images= read_files(directory)
with open('svm_model_edge.pkl' , 'rb') as f :
    model = cPickle.load(f)

cpt=0
for i in images :
   
   path = './tiled/%s'%i
   img = extract_feature_edge(path) 
   img = img.reshape(1, -1)
   label=model.predict(img)
   print(i,'',label) 
   
   
   if (label =="edges") :
      cpt=cpt+1
      os.remove(path)


print("%d Deleted images !!!"%cpt)




#Loading the model using torch hub
print('Now we will start the detection')
#*********************************************************CUSTOM**********************************************
#model = torch.hub.load('./', 'custom', path='best.pt', source='local')
model.conf = 0.70


#############Default pretrained model##############################################
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

#Reading the new images so that we can make the batch inference
folder="./tiled/"
imgs = []
files = os.listdir(directory)
for filename in files:
   imgs.append(folder+filename)





#Inference
results = model(imgs, size=416)
#results.save()
#create a list to concatenate the pandas
results_list=[] 
for x in range(0,len(imgs)):
   results_list.append(results.pandas().xyxy[x])

#concatenate the pandas    
finale_result=pd.concat(results_list)
helmets=finale_result.loc[finale_result['class'] == 0, 'class'].count()
heads=finale_result.loc[finale_result['class'] == 1, 'class'].count()

print("Number of helmets detected", helmets)
print("Number of heads without helmets detected", heads)

#Delete the tiles :
print("deleting the tiles")
tile_dir = './tiled'
for f in os.listdir(tile_dir):
    os.remove(os.path.join(tile_dir, f))





#Convert pandas to json
#json_results = finale_result.to_json(orient="records")
#print(json_results)



print("Detection finished !")

