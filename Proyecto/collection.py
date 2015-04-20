'''
Created on 14/4/2015

@author: Psilocibino
'''
import cv2
import numpy as np
import ImageTk, Image
from matplotlib.cbook import Null

class collection:
    name = ''
    info = ''
    img = None
    id = -1
    
    def __init__(self,img,name,info):
        self.name = name
        self.info = info
        if(img!=None):
            self.img = img
        else:
            self.img = 'no-image.png'
    
    def get_name(self):
        return self.name
    
    def get_info(self):
        return self.info
    
    def get_img(self):
        return self.img
    
    def set_id(self,i):
        self.id = i