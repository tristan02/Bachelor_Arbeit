'''
Created on 2/12/2014

@author: Tristan
'''
import cv2
import numpy as np
from Proyecto.butterfly import butterfly
import tkMessageBox
import ImageTk, Image
from matplotlib.cbook import Null


class database:
    
    data_checked = []
    data_unchecked = []
    
    def __init__(self):
        pass
    
    #Agregamos una nueva mariposa sin procesar a la base de datos
    def new_but(self,but):
        new = True
        for elem in self.data_unchecked:
            n1 = but.get_name()
            n2 = elem.get_name()
            if n1 == n2:
                new = False
        if new:        
            self.data_unchecked.append(but)
            return 0
        else:
            return -1
        
    def reescale_bd(self,d):
        for elem in self.data_unchecked:
            if not((elem.get_dist03() + 3) > d and (elem.get_dist03() - 3) < d):
                elem.reescale(d)
            if elem.get_centroide() != 0:
                elem.reescale_mask()
            
    #Sacamos
    def get_last_but_uncp(self):
        return self.data_unchecked.pop()
    
    def get_count_but(self):
        return len(self.data_unchecked)
    
    def get_but(self,i):
        if i < self.get_count_but():
            return self.data_unchecked[i]
    
    def save_db(self):
        file = open('db.txt','w')
        file.write(str(self.get_count_but()) + '\n')
        
        for elem in self.data_unchecked:
            file.write(elem.get_name() + '\n')
            file.write(str(elem.get_broken()) + '\n')
            file.write(str(elem.get_checked()) + '\n')
            file.write(str(elem.get_reescaled()) + '\n')
            
        file.close()
        
    def load_db(self,path):
        file = open(path, 'r')
        n = int(file.readline())
        
        for i in range(n):
            h = file.readline()
            h = h[:len(h)-1]            
            img = np.array(Image.open(h))
            b = butterfly(img,h)
            
            br = file.readline()
            br = br[:len(br)-1]
            b.set_broken(br)
            
            ch = file.readline()
            ch = ch[:len(ch)-1]
            b.set_checked(ch)
            
            re = file.readline()
            re = re[:len(re)-1]
            b.set_reescaled(re)
            
            self.new_but(b)
            
    def delete_db(self):
        #Hay que destruir todas las mariposas????
        self.data_unchecked = []
        
        
        
        
        
        
        
        
        
        