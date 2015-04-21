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
from matplotlib.mlab import donothing_callback
from collection import collection
import os


class database:
    
    data_collection = []
    data_unchecked = []
    data_checked = []
    num_but = 0
    num_col = 0
    
    def __init__(self):
        col1 = collection(None,'Europa','Esta collection es muy completa. Es la hostia.')
        col2 = collection(None,'Africa','Esta collection es muy completa. Es la hostia.')
        self.data_collection.append(col1)
        self.data_collection.append(col2)
        
        i = np.array(Image.open('img (2).jpg'))  
        but1 = butterfly(i,'but1')
        i = np.array(Image.open('img (3).jpg'))
        but2 = butterfly(i,'but2')
        
        self.data_checked = {col1.get_name():[but1,but2],col2.get_name():[]}
        
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
        
    def del_item(self,col,but):
        valor = self.data_checked[col]
        valor.remove(but)
        self.data_checked[col] = valor
        
    def new_col(self,col):
        new = True
        for elem in self.data_collection:
            n1 = col.get_name()
            n2 = elem.get_name()
            if n1 == n2:
                new = False
        if new:        
            self.data_collection.append(col)
            self.data_checked[col.get_name()] = []
            return 0
        else:
            return -1
        
    def get_cols(self):
        cols = []
        for elem in self.data_collection:
            cols.append(elem.get_name())
        return cols
    
    def get_buts_col(self,col):
        i = self.data_checked[col]
        return i
    
    def get_info_col(self,col_act):
        for elem in self.data_collection:
            if col_act == elem.get_name():
                return (elem.get_info(),elem.get_img())
        return ('0','0')
            
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
        
        
        
        
        
        
        
        
        
        