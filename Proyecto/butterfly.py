'''
Created on 2/12/2014

@author: Tristan
'''
import cv2
import numpy as np
import ImageTk, Image
from matplotlib.cbook import Null
from Proyecto.build_mask import build_mask
from Proyecto.build_mask import rebuild_moments
from Proyecto.get_histogram import get_hist


class butterfly:
    broken = False
    #Cada vez que reescalamos utilizaremos esta copia y asi no perdemos calidad
    orig_img = Null
    np_img = Null
    pil_img = Null
    min_img = Null
    orig_mask_img = Null
    mask_img = Null
    hist_img = Null
    hist = []
    name = ''
    dist03 = 0
    area = 0
    centroide = (0,0)
    orig_w = 0
    orig_h = 0
    w = 0
    h = 0
    contour = []
    
    def __init__(self,img,name):
        self.np_img = img
        self.orig_img = img
        self.pil_img = ImageTk.PhotoImage(Image.fromarray(img))
        self.name = name
        self.w = self.pil_img.width()
        self.h = self.pil_img.height()
        self.orig_w = self.pil_img.width()
        self.orig_h = self.pil_img.height()
        #Creamos la imagen en miniatura
        aux = cv2.resize(img,(self.w/2, self.h/2), interpolation = cv2.INTER_CUBIC)
        self.min_img = ImageTk.PhotoImage(Image.fromarray(aux))
        #Sacamos la mascara, centroide y area
        self.contour,self.orig_mask_img,self.centroide,self.area = build_mask(self.orig_img)
        self.mask_img = self.orig_mask_img
        #Calculamos el histograma con su imagen
        self.hist_img,self.hist = get_hist(self.np_img,self.mask_img)
    
    #A partir de la medida entre el 0 y el 3 que son "3cmm" reescalamos a escala 2:1
    def reescale(self,d):
        k = float(d)/float(self.dist03)
        self.w = int(self.orig_w*k)
        self.h = int(self.orig_h*k)
        self.np_img = cv2.resize(self.orig_img,(self.w, self.h), interpolation = cv2.INTER_CUBIC)
        self.pil_img = ImageTk.PhotoImage(Image.fromarray(self.np_img))
        self.mask_img = cv2.resize(self.orig_mask_img,(self.w, self.h), interpolation = cv2.INTER_CUBIC)
        self.contour,self.area = rebuild_moments(self.mask_img)
        self.mask_img = cv2.resize(self.orig_mask_img,(self.w, self.h), interpolation = cv2.INTER_CUBIC)
    
    #Dist03 sera la distancia en pixeles que hay entre el 0 y el 3 de la escala metrica      
    def get_dist03(self):
        return self.dist03
        
    def get_mask(self):
        return self.mask_img
    
    def get_hist_img(self):
        return self.hist_img
    
    def get_hist(self):
        return self.hist
    
    def get_cnt(self):
        return self.contour
    
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
    
    def get_size(self):
        return self.h,self.w
    
    def get_centroide(self):
        return self.centroide
    
    def get_area(self):
        return self.area
    
    def set_dist03(self,d):
        self.dist03 = d
        
    def set_centroide(self,x,y):
        self.centroide = (x,y)
            
    def set_area(self,a):
        self.area = a
    
    #Cambiamos el valor de broken en caso de que la nueva muestra este daada
    def set_broken(self,s):
        if s == "yes" or s == 'True':
            self.broken = True
            
    def set_pil_img(self,img):
        self.pil_img = img
    
    def set_img_min(self,img):
        self.img_min = img
        
    