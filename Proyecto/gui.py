'''
Created on 2/12/2014

@author: Tristan
'''
import cv2
import numpy as np
from Proyecto.butterfly import butterfly
from Proyecto.database import database
from Proyecto.menus import menus
from matplotlib.cbook import Null
import Tkinter as tk
import Combobox



if __name__ == '__main__':
    
    db = database()
    
    root = tk.Tk()
    root.geometry("750x500") 

    menu = menus(root,db)
    #box = Combobox(root)
    root.mainloop()
    
    
      







