import time
import os 
import urllib.request, json 
import timeit





    
while True:
    #import the json data
    with urllib.request.urlopen("http://timelapsestorage.s3.amazonaws.com/test/test.json") as url:
        data = json.loads(url.read().decode())
        #print(data)

    #get the liste of s3ids and images' names
    liste=data['datas']

    #Create the full URL liste
    #url=[]
    base="s3://timelapsestorage/"
    
    for x in range(0,len(liste)):
        l=liste[x]
        s3id=l['s3id']
        s3img=l['img']
    
        link=base+s3id+"/HIGH/"+s3img
        #url.append(link)
        #COMMAND TO UPLOAD THE FILE#################################################################     



    
        path = "./totile"
        dir = os.listdir(path)

        def isEmpty():
            if len(dir) == 0:
                print("empty")
                return True
            else:
                print("not empty")
                print(dir[0])
                return False 
        
        
        c=isEmpty() ; 
        print(c)
    
        if c==False :
            start = time.time()
            for i in range(0,len(dir)) :
                img_name=dir[i]
                img_path = './totile/%s'%img_name

                print(img_path)
                os.system("python tile_withdirectory.py %s %s %s"%(img_path,s3id,s3img))
                print("tiling done !!")
                os.remove(img_path)
                print("image is deleted")
            
            dir.clear()
            end = time.time()
            print("Time elapsed :", end - start)

     


    
    
   

    time.sleep(3)



  
# Getting the list of directories
#dir = os.listdir(path)
  
# Checking if the list is empty or not



