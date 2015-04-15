'''
Created on 15/4/2015

@author: Psilocibino
'''
from matplotlib.cbook import Null
from Tkinter import *
import ttk
from Tkconstants import BOTH, TOP, LEFT, BOTTOM, RIGHT
import cv2
import numpy as np
from Proyecto.butterfly import butterfly
import ImageTk, Image
from collection import collection
from menu import *
from tkFileDialog import *
from menu import MenuDemo


class dialog_new_col:
    root = None
    e1 = None
    img = Null
    
    def __init__(self):
        self.root = Tk()
        frame = Frame(self.root,name='dialog_new_col', width=200, height=200)
        self.root.title('Nueva coleccion...')
        frame.pack()
        
        label = Label(frame, text="Nombre de la nueva coleccion:") 
        self.e1 = Entry(frame, bd =5)
        self.subir_foto = Button(frame, text="Subir foto...", command=self.foto_col) 
        self.crear = Button(frame, text="Crear", command=self.crear)
        
        label.pack(side=LEFT)
        self.e1.pack(side = RIGHT)
        self.subir_foto.pack(side=LEFT) 
        self.crear.pack(side=RIGHT)
        
        label.grid(row=0, column=0)
        self.e1.grid(row=0, column=1)
        self.subir_foto.grid(row=1, column=0)
        self.crear.grid(row=1, column=1)
            
        self.root.mainloop()
        
    def crear(self):
        n = self.e1.get()
        col = collection(self.img,n)
        MenuDemo.db.new_col(col)
        self.root.quit()
        
    def foto_col(self):
        f = str(askopenfile())
        path = get_path(f)
        self.img = np.array(Image.open(path)) 
        
class dialog_edit_but:
    def __init__(self):
        self.root = Tk()
        frame = Frame(self.root,name='dialog_edit')
        self.root.title('Editar...')
        frame.pack()
        
        label = Label(frame, text="Opciones:")
        self.del_but = Button(frame, text="Eliminar mariposa", command=self.delete_but) 
        self.ins_but = Button(frame, text="Insertar en base de datos", command=self.comparar)
        
        label.pack(side=LEFT)
        self.del_but.pack(side=LEFT) 
        self.ins_but.pack(side=LEFT)
        
        label.grid(row=0, column=0)
        self.del_but.grid(row=1, column=0)
        self.ins_but.grid(row=2, column=0)
            
        self.root.mainloop()   
    def delete_but(self):
        MenuDemo.but_act = Null
        im = Image.open('new.png')
        imh = ImageTk.PhotoImage(im)
        MenuDemo.update_but_frame(MenuDemo(),imh) 
                
    def comparar(self):
        '''TODO'''
        donothing_callback() 
