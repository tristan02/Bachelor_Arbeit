'''
Created on 10/2/2015

@author: Psilocibino
'''
from Tkinter import *
from matplotlib.cbook import Null
import ttk

'''Con esta clase seremos capaces de acceder a cada una de las 
mariposas para eliminarlas o compararla con las demas'''
class Combobox:
    w = Null
    value_of_combo = 'Mariposa a seleccionar'

    def __init__(self, w):
        self.w = w
        
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.w, textvariable=self.box_value)
        self.box['values'] = ('1', '2', '3')
        #TODO aqui deberan aparecer todas las mariposas
        self.box.current(0)
        self.box.grid(column=0, row=0)