#!/usr/local/bin/python2
import os
from random import randint

class FileHandler(object):
    def __init__(self):
        pass
    def switch(self,path):
       filenames = [f for f in os.listdir(path)]
#       print(filenames)
       arrlen = len(filenames)
       fIndex = randint(0, arrlen-1)
       sIndex = randint(0, arrlen-1)
       while (fIndex==sIndex):
           sIndex = randint(0,arrlen-1)
       print('switching '+str(filenames[fIndex])+' and '+str(filenames[sIndex]))
       f_name = filenames[fIndex]
       s_name = filenames[sIndex]
       os.rename(path+"/"+filenames[sIndex], path+"/tmp")
       os.rename(path+"/"+filenames[fIndex], path+"/"+s_name)
       os.rename(path+"/tmp", path+"/"+f_name)

if __name__ == "__main__":
   fh = FileHandler()
   fh.switch('/media/fengchang/stream/split')
