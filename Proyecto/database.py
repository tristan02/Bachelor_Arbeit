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
    data_checked = {}
    num_but = 0
    num_col = 0
    d = 0
    
    def __init__(self):
        '''col1 = collection(None,'Europa','Esta collection es muy completa. Es la hostia.')
        col2 = collection(None,'Africa','Esta collection es muy completa. Es la hostia.')
        self.data_collection.append(col1)
        self.data_collection.append(col2)
        
        i = np.array(Image.open('img (2).jpg'))  
        but1 = butterfly(i,'but1')
        i = np.array(Image.open('img (3).jpg'))
        but2 = butterfly(i,'but2')
        
        self.data_checked = {col1.get_name():[but1,but2],col2.get_name():[]}'''
        
    #Agregamos una nueva mariposa sin procesar a la base de datos
    def new_but(self,but,col):
        new = True
        for elem in self.data_unchecked:
            n1 = but.get_name()
            n2 = elem.get_name()
            if n1 == n2:
                new = False
        if new:        
            aux = []
            aux = self.data_checked[col]
            aux.append(but)
            self.data_checked[col] = aux
            #self.reescale_bd(but.get_dist03())
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
            
    def reescale_bd(self):
        self.d = 0
        error = 0
        c = self.db.get_count_but()
        for i in range(c):
            but = self.db.get_but(i)
            #Si la imagen ya ha sido reescalada no buscamos su distancia pues ya la sabemos but.dist03
            dist = but.get_dist03()
            #Si la medida sale mal la sacamos de la media
            if dist > 10:
                self.d = self.d + dist
            else:
                ''''TODO Si no se ha detectado bien el 03 hay que hacer algo!'''
                #self.db.delete_but(but)
                error = error + 1
        self.d = self.d/(c-error)
        
        for elem in self.data_checked:
            if not((elem.get_dist03() + 3) > self.d and (elem.get_dist03() - 3) < self.d):
                elem.reescale(self.d)
            if elem.get_centroide() != 0:
                elem.reescale_mask()
        print self.d
            
    #Sacamos
    def get_last_but_unch(self):
        return self.data_unchecked.pop()
    
    def get_count_but(self):
        return len(self.data_checked)
    
    def get_but(self,i):
        if i < self.get_count_but():
            return self.data_unchecked[i]
    
    def save_db(self,last_col):
        file = open('db.txt','w')
        file.write(str(len(self.get_cols())) + '\n')
               
        for col in self.data_collection:
            buts = self.get_buts_col(col.get_name())                        
            file.write(col.get_name() + '\n')
            file.write(col.get_info() + '\n')
            #file.write(col.get_img() + '\n')  
            file.write(str(len(buts)) + '\n')
                      
            for elem in buts:               
                file.write(elem.get_name() + '\n')
                file.write(str(elem.get_broken()) + '\n')
                x,y = elem.get_centroide()
                file.write(str(x) + ',' + str(y) + '\n')
                file.write(str(elem.get_dist03()) + '\n')
                file.write(str(elem.get_area()) + '\n')
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
        self.data_checked = {}
        
        
        
        
        
        
        
        
        
        