import cv2
import math
import os
import sys

Path= sys.argv[1]
s3id=sys.argv[2]
s3img=sys.argv[3]


filename, file_extension = os.path.splitext(Path)

image = cv2.imread(Path)


#Get the exact image name 
filename_split = filename.split("/")
image_name = filename_split[2]

Directory="./tiled/%s"%image_name  
print(Directory)

tileSizeX = 416
tileSizeY = 416
numTilesX = math.ceil(image.shape[1]/tileSizeX)
numTilesY = math.ceil(image.shape[0]/tileSizeY)




makeLastPartFull = True; # in case you need even siez

for nTileX in range(numTilesX):
    for nTileY in range(numTilesY):
        startX = nTileX*tileSizeX
        endX = startX + tileSizeX
        startY = nTileY*tileSizeY
        endY = startY + tileSizeY

        if(endY > image.shape[0]):
            endY = image.shape[0]

        if(endX > image.shape[1]):
            endX = image.shape[1]

        if( makeLastPartFull == True and (nTileX == numTilesX-1 or nTileY == numTilesY-1) ):
            startX = endX - tileSizeX
            startY = endY - tileSizeY

        currentTile = image[startY:endY, startX:endX]
        cv2.imwrite(Directory + '_%d_%d' % (nTileY, nTileX)  + file_extension, currentTile)

print("The image is tiled now we will start the classification !")

os.system("python makeinference.py ./tiled %s %s"%(s3id,s3img))