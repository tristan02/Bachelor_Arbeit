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
from numpy.f2py.rules import aux_rules


class database:
    
    data_collection = []
    data_checked = {}
    num_but = 0
    num_col = 0
    d = 0
    col_act = '-'
    
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
        
        try:
            self.load_db('db.txt')
        except:
            print ('Error de carga de base de datos')
        
    #Agregamos una nueva mariposa sin procesar a la base de datos
    def new_but(self,but,col):
        new = True
        'TODO: Comprobar que el nombre no esta repetido'
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
        
    def del_col(self,col):
        for elem in self.data_collection:
            if elem.get_name() == col:
                self.data_collection.remove(elem)
                break
        del self.data_checked[col]
        
    def rename_col(self,col,n_name):
        aux = 0
        for elem in self.data_collection:
            if elem.get_name() == col:
                self.data_collection[aux].set_name(n_name)
                break
            aux = aux + 1
        
        self.data_checked[n_name] = self.data_checked[col]
        del self.data_checked[col]

        
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
        buts = []
        if col != '':
            for elem in self.data_checked[col]:
                buts.append(elem)            
        return buts
    
    def get_buts(self):
        cols = self.get_cols()
        buts = []
        for col in cols:
            buts_col = self.get_buts_col(col)
            buts = buts + buts_col
            
        return buts
    
    def get_col_from_but(self, but):
        cols = self.get_cols()
        
        for col in cols:
            buts_col = self.get_buts_col(col)
            i = 0
            for elem in buts_col:
                if elem == but:
                    return col,i 
                i = i + 1
    
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
    
    def get_count_but(self):
        return len(self.data_checked)
        
    def get_col_act(self):
        return self.col_act
        
    def save_db(self,last_col):
        file = open('db.txt','w')        
        file.write(str(len(self.get_cols())) + '\n')
        file.write(last_col  + '\n')
               
        for col in self.data_collection:
            buts = self.get_buts_col(col.get_name())                        
            file.write(col.get_name() + '\n')
            file.write(col.get_info() + '\n' + '\n')
            #file.write(col.get_img() + '\n')  
            file.write(str(len(buts)) + '\n')
                      
            for elem in buts:               
                file.write(elem.get_name() + '\n')
                file.write(str(elem.get_broken()) + '\n')
                x,y = elem.get_centroide()
                file.write(str(x) + '\n')
                file.write(str(y) + '\n')
                file.write(str(elem.get_dist03()) + '\n')
                file.write(str(elem.get_area()) + '\n')    
        file.close()
        
    def load_db(self,path):
        file = open(path, 'r')        
        num_cols = int(file.readline())
        self.col_act = file.readline()
        self.col_act = self.col_act[:len(self.col_act)-1]
        
        for i in range(num_cols):
            col_name = file.readline()
            col_name = col_name[:len(col_name)-1]
           
            aux = file.readline()
            col_info = ''
            while (aux != '\n'):
                aux = aux[:len(aux)-1]
                col_info = col_info + aux
                aux = file.readline()
            #col_img = file.readline()            
            col = collection(None,col_name,col_info)
            self.new_col(col)
            try:
                num_buts = int(file.readline())
            except:
                file.readline()
                num_buts = int(file.readline())
                
            for j in range(num_buts):
                path = file.readline()
                path = path[:len(path)-1]            
                img = np.array(Image.open(path))
                b = butterfly(img,path)
                
                br = file.readline()
                br = br[:len(br)-1]
                b.set_broken(br)
                
                centr_x = file.readline()
                x = float(centr_x[:len(centr_x)-1])
                centr_y = file.readline()
                y = float(centr_y[:len(centr_y)-1])
                b.set_centroide(x,y)
                
                d03 = file.readline()
                d03 = int(d03[:len(d03)-1])
                b.set_dist03(d03)
                
                area = file.readline()
                area = float(area[:len(area)-1])
                b.set_area(area)
                
                self.new_but(b,col.get_name())
        
        return 
            
    def delete_db(self):
        self.data_checked = {}
        self.data_collection = []   
        