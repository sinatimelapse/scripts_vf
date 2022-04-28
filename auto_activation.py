import time
import os 

import timeit
while True:
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
            os.system("python tile_withdirectory.py %s"%img_path)
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



