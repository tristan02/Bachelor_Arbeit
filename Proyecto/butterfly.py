'''
Created on 2/12/2014

@author: Tristan
'''
import cv2
import numpy as np
import ImageTk, Image
from matplotlib.cbook import Null
from Proyecto.get_mask import get_mask
from Proyecto.get_histogram import get_hist


class butterfly:
    broken = False
    checked = False
    #TODO quitar reescaled. no sirve de mucho. mejor basarse en si tenemos o no la distancia 03 real y ya esta.
    reescaled = False
    orig_img = Null
    np_img = Null
    pil_img = Null
    min_img = Null
    mask_img = Null
    hist_img = Null
    name = ''
    dist03 = 0
    area = 0
    centroide = (0,0)
    w = 0
    h = 0
    
    def __init__(self,img,name):
        self.np_img = img
        self.orig_img = img
        self.pil_img = ImageTk.PhotoImage(Image.fromarray(img))
        self.name = name
        self.w = self.pil_img.width()
        self.h = self.pil_img.height()
        #Creamos la imagen en miniatura
        aux = cv2.resize(img,(self.w/4, self.h/4), interpolation = cv2.INTER_CUBIC)
        self.min_img = ImageTk.PhotoImage(Image.fromarray(aux))
    
    #A partir de la medida entre el 0 y el 3 que son "3cmm" reescalamos a escala 2:1
    def reescale(self,d):
        k = float(d)/float(self.dist03)
        self.w = int(self.w*k)
        self.h = int(self.h*k)
        self.np_img = cv2.resize(self.np_img,(self.w, self.h), interpolation = cv2.INTER_CUBIC)
        self.pil_img = ImageTk.PhotoImage(Image.fromarray(self.np_img))
        self.reescaled = False
        #Redefinimos la miniimagen
        i = cv2.resize(self.np_img,(self.w/4, self.h/4), interpolation = cv2.INTER_CUBIC)
        self.min_img = ImageTk.PhotoImage(Image.fromarray(i))
        #Reescalamos la maskara
        self.reescale_mask()
    
    #Basandonos en dist03 reescalamos las maskara  
    def reescale_mask(self):
        if self.area != 0:
            self.mask_img = cv2.resize(self.mask_img,(self.w, self.h), interpolation = cv2.INTER_CUBIC)
            
    #Dist03 sera la distancia en pixeles que hay entre el 0 y el 3 de la regla      
    def get_dist03(self):
        return self.dist03
    
    def get_mask(self):
        if self.area == 0 and not(self.reescaled):
            self.mask_img,self.centroide,self.area = get_mask(self.np_img)
        elif self.area == 0 and self.reescaled:
            self.mask_img,self.centroide,self.area = get_mask(self.orig_img)
            self.reescale_mask()
        
        #cv2.imwrite(self.name + '_mask.jpg', self.mask_img)
        return self.mask_img
    
    def get_hist(self):
        if self.area == 0 and not(self.reescaled):
            self.get_mask()
            self.hist_img = get_hist(self.np_img,self.mask_img)
        else:
            self.hist_img = get_hist(self.np_img,self.mask_img)
        return self.hist_img
    
    #Getter de la imagen en np
    def get_np_img(self):
        return self.np_img
    
    #Getter de la imagen en pil para ser mostrada en la GUI
    def get_pil_img(self):
        return self.pil_img
        
    def get_min_img(self):
        return self.min_img
    
    def get_name(self):
        return self.name
    
    def get_w(self):
        return self.w
    
    def get_h(self):
        return self.h
    
    def get_broken(self):
        return self.broken
    
    def get_checked(self):
        return self.checked
    
    def get_reescaled(self):
        return self.reescaled
    
    def get_size(self):
        return self.h,self.w
    
    def get_centroide(self):
        return self.centroide
       
    def set_dist03(self,d):
        self.dist03 = d
        
    def set_centroide(self,x,y):
        self.centroide = (x,y)
    
    def set_checked(self,c):
        if c == 'True':
            self.checked = True
            
    def set_reescaled(self,c):
        if c == 'True':
            self.checked = True
    
    #Cambiamos el valor de broken en caso de que la nueva muestra este daada
    def set_broken(self,s):
        if s == "yes" or s == 'True':
            self.broken = True
            
    def set_pil_img(self,img):
        self.pil_img = img
    
    def set_img_min(self,img):
        self.img_min = img
        
    