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
        c = self.get_count_cols()
        cols = self.get_cols()
        count = 0
        #Calculamos la media de todas las dist03
        for i in range(c):
            buts = self.get_buts_col(cols[i])
            for j in range(len(buts)):
                but = buts[j]
                dist = but.get_dist03()
                self.d = self.d + dist 
                count = count + 1       
        self.d = self.d/(count)
        
        for i in range(c):
            buts = self.get_buts_col(cols[i])
            for j in range(len(buts)):
                but = buts[j]
                but.reescale(self.d)
    
    def get_count_cols(self):
        return len(self.data_checked)
        
    def get_col_act(self):
        return self.col_act
        
    def save_db(self,last_col):
        doc = open('db.txt','w')
        #Numero de colecciones existentes en la base de datos        
        doc.write(str(len(self.get_cols())) + '\n')
        doc.write(last_col  + '\n')
               
        for col in self.data_collection:
            buts = self.get_buts_col(col.get_name())                        
            doc.write(col.get_name() + '\n')
            doc.write(col.get_info() + '\n' + '\n')
            #doc.write(col.get_img() + '\n')  
            doc.write(str(len(buts)) + '\n')
                      
            for elem in buts:               
                doc.write(elem.get_name() + '\n')
                doc.write(str(elem.get_broken()) + '\n')
                x,y = elem.get_centroide()
                doc.write(str(x) + '\n')
                doc.write(str(y) + '\n')
                doc.write(str(elem.get_dist03()) + '\n')
                doc.write(str(elem.get_area()) + '\n')    
        doc.close()
        
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
            while not(isinstance( aux, int )):
                aux = aux[:len(aux)-1]
                col_info = col_info + aux
                aux = file.readline()
                try:
                    aux = int(aux)
                except:
                    pass
            #col_img = file.readline()            
            col = collection(None,col_name,col_info)
            self.new_col(col)
            
            num_buts = aux
                
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
            
        self.reescale_bd()        
        return 
            
    def delete_db(self):
        self.data_checked = {}
        self.data_collection = []   
        