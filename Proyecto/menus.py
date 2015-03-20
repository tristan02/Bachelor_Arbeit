'''
Created on 2/12/2014

@author: Tristan
'''
import cv2
import numpy as np
from Tkinter import *
from Proyecto.butterfly import butterfly
import ImageTk, Image
from tkFileDialog import *
from Proyecto.menus import *
import tkMessageBox
from Proyecto.resize import find_0_3
from matplotlib.cbook import Null
from matplotlib.mlab import donothing_callback
import ttk
from Proyecto.database import database
import os

#Construccion del menus y submenus
class menus:

    w = Null
    db = Null
    but_act = Null
    frame = Null
    panel = Null
    grid = Null
    
    def __init__(self,w,db):
        self.w = w
        menubar = Menu(w)
        self.db = db
        self.frame = Frame(self.w)
        self.frame.bind("<Button-1>", self.callback)
        self.frame.pack()
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load new item...", command=self.load_but)
        filemenu.add_command(label="Load Database", command=self.load_db)
        filemenu.add_command(label="Save Database", command=self.db.save_db)
        filemenu.add_command(label="Close", command=self.close_but)        
        filemenu.add_separator()        
        filemenu.add_command(label="Exit", command=w.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Rescale", command=self.resize)
        editmenu.add_command(label="Show masks", command=self.show_masks)
        editmenu.add_command(label="Show histograms", command=self.show_hist)  
        editmenu.add_command(label="Show butterflies", command=self.refresh_grid)       
        editmenu.add_separator()        
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)        
        menubar.add_cascade(label="Edit", menu=editmenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        w.config(menu=menubar)
        
        #Para no tener que cargar cada vez la base de datos
        self.db.load_db('db.txt')
        self.refresh_grid()
        
    def callback(self,event):
        print "clicked at", event.x, event.y
               
    def donothing(self):
        pass
    
    #Par de bucles para extraer la ruta de la imagen que hemos seleccionado en el explorador
    def get_path(self,s):
        aux = 0
        p = ""
        for i in s:
            if i == "'":
                p = s[aux+1:]
                break
            aux += 1
        aux = 0
        for i in p:
            if i == "'":
                p = p[:aux]
                break
            aux += 1
        return p
    
    #Carga una imagen deseada, crea una mariposa, la muestra, pregunta si esta rota y la guarda en la bd
    def load_but(self):
        b = str(askopenfile())
        path = self.get_path(b)
        i = np.array(Image.open(path))
        #Creamos la mariposa
        name = 'ima/' + os.path.basename(path)
        self.but_act = butterfly(i,name)
        self.refresh_panel(self.but_act.get_pil_img())
        
        s = tkMessageBox.askquestion("Integridad", "Le falta algun trozo al ejemplar?")        
        self.but_act.set_broken(s)
        if self.db.new_but(self.but_act) == -1:
            self.refresh_grid()
            tkMessageBox.showinfo(None, "La mariposa ya esta en la base de datos o se ha producido un error")
        else:
            tkMessageBox.showinfo(None, "La mariposa ha sido aniadida a la base de datos, aunque todavia no pa sido procesada.")
        #self.w.mainloop()
    
    def close_but(self):
        if self.panel != Null:
            self.panel.destroy()
        self.frame.destroy()
        self.db.delete_db()
        
    def show_masks(self):        
        c = self.db.get_count_but()
        for i in range(c):
            but = self.db.get_but(i)
            cv2.imshow(but.get_name(), but.get_mask())
     
    #De momento abrimos una ventana con el histograma de cada mariposa       
    def show_hist(self):
        c = self.db.get_count_but()
        for i in range(c):
            but = self.db.get_but(i)
            cv2.imshow(but.get_name(), but.get_hist())
    
    #Para intentar perder la menor informacion posible sobre las imagenes,
    # el nuevo tamanyo sera segun la media de las distancias
    def resize(self):
        d = 0
        error = 0
        c = self.db.get_count_but()
        for i in range(c):
            but = self.db.get_but(i)
            #Si la imagen ya ha sido reescalada no buscamos su distancia pues ya la sabemos but.dist03
            if not(but.get_reescaled()):
                dist = find_0_3(but.get_np_img())
            else:
                dist = but.get_dist03()
            #Si la medida sale mal la sacamos de la media
            if dist > 10:
                d = d + dist
                but.set_dist03(dist)
            else:
                #TODO Si no se ha detectado bien el 03 hay que hacer algo!
                #self.db.delete_but(but)
                error = error + 1
        d = d/(c-error)
        self.db.reescale_bd(d)
        self.refresh_grid()
        self.w.mainloop()
        
    def refresh_panel(self,img):        
        if self.panel != Null:
            self.panel.destroy()
        try:
            self.frame.destroy()
            self.frame = Frame(self.w)
            self.panel = Label(self.frame, image = img)
            self.frame.pack()
            self.panel.pack(side = "top", fill = "none", expand = "yes")
            
        except IOError:
            self.panel.destroy()
            
    def refresh_grid(self):
        r = 0
        for i in range(self.db.get_count_but()):
            b = self.db.get_but(i)
            if self.panel != Null:
                self.panel.destroy()
            panel = Label(self.frame, image=b.get_min_img() ,borderwidth=1 ).grid(row=r,column=0)
            r = r + 1
        #self.w.mainloop()
        
    
    def load_db(self):
        b = str(askopenfile())
        path = self.get_path(b)
        self.db.load_db(path)
        self.refresh_grid()     
        
    
if __name__ == '__main__':
    
    db = database()
    
    root = Tk()
    root.geometry("750x500") 

    menu = menus(root,db)
    #box = Combobox(root)
    root.mainloop()
    
    