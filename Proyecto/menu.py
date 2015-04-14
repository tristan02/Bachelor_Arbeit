'''
Created on 24/3/2015

@author: Psilocibino
'''
from Tkinter import *
import ttk
from panels import SeePanel
from Tkconstants import BOTH, TOP, LEFT, BOTTOM, RIGHT
import cv2
import numpy as np
from Proyecto.butterfly import butterfly
import ImageTk, Image
from tkFileDialog import *
from Proyecto.menus import *
import tkMessageBox
from Proyecto.resize import find_0_3
from matplotlib.mlab import donothing_callback
from Proyecto.database import database
from Proyecto.collection import collection
import os
from matplotlib.cbook import Null
from doctest import master
 
class MenuDemo(ttk.Frame):
    
    w = Null
    but_act = Null
    frame = Null
    panel = Null
    grid = Null
    img = Null
    db = database()
     
    def __init__(self, name='menudemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(fill=BOTH)
        self.master.title('Buterflies Database')
        self._create_panel()
        self.db = database() 
    
    def _create_panel(self):
        Panel = Frame(self, name='panel')
        Panel.pack(side=TOP, fill=BOTH)
         
        msg = ["Butterflies Database"]
         
        lbl = ttk.Label(Panel, text=''.join(msg), wraplength='4i', justify=LEFT)
        lbl.pack(side=TOP, padx=5, pady=5)
        
        #Button collection
        im = Image.open('upload.jpg')
        imh = ImageTk.PhotoImage(im)
        codeBtn = ttk.Button(text='New Collection...', image=imh, default=ACTIVE, command=self.new_col)
        codeBtn.image = imh
        codeBtn['compound'] = LEFT
        #codeBtn.focus()
        codeBtn.grid(in_=self, row=1, column=0, sticky=E)
        codeBtn.pack(side=LEFT)
        
        #Button nueva mariposa
        im = Image.open('new.png')
        imh = ImageTk.PhotoImage(im)
        codeBtn = ttk.Button(text='New Butterfly...', image=imh, default=ACTIVE, command=self.load_but)
        codeBtn.image = imh
        codeBtn['compound'] = LEFT
        #codeBtn.focus()
        codeBtn.grid(in_=self, row=1, column=0, sticky=E)
        codeBtn.pack(side=LEFT)
         
        # create statusbar
        statusBar = ttk.Frame()
        self.__status = ttk.Label(self.master, text=' ', borderwidth=1,
                              font=('Helv 10'), name='status')
         
        self.__status.pack(side=LEFT, padx=2, fill=BOTH)
        statusBar.pack(side=BOTTOM, fill=X, pady=2)
                 
        # create the main menu (only displays if child of the 'root' window)
        self.master.option_add('*tearOff', False)  # disable all tearoff's
        self._menu = Menu(self.master, name='menu')
        self._build_submenus()
        self.master.config(menu=self._menu)
         
        # set up standard bindings for the Menu class
        # (essentially to capture mouse enter/leave events)
        self._menu.bind_class('Menu', '<<MenuSelect>>', self._update_status)
 
    def _build_submenus(self):
        # create the submenus
        # the routines are essentially the same:
        #    1. create the submenu, passing the main menu as parent
        #    2. add the submenu to the main menu as a 'cascade'
        #    3. add the submenu's individual items
         
        self._add_file_menu()
        self._add_basic_menu()
        self._add_cascades_menu()
        self._add_colors_menu()
 
    # ================================================================================
    # Submenu routines
    # ================================================================================
 
    # File menu ------------------------------------------------------------------               
    def _add_file_menu(self):
        filemenu = Menu(self._menu, name='filemenu')
        self._menu.add_cascade(label='File', menu=filemenu, underline=0)
 
        filemenu.add_command(label='Load new item...',command=self.load_but)
        filemenu.add_command(label="Load new colection...", command=self.new_col)
        filemenu.add_command(label="Load Database", command=self.load_db)
        #filemenu.add_command(label="Save Database", command=self.db.save_db)
        filemenu.add_command(label="Close", command=self.close_but)   
        filemenu.add_separator()
        filemenu.add_command(label='Exit',
                          command=lambda: self.master.destroy()) # kill toplevel wnd
         
    # Basic menu ------------------------------------------------------------------       
    def _add_basic_menu(self):
        bmenu = Menu(self._menu)
        self._menu.add_cascade(menu=bmenu, label='Basic', underline=0)
        bmenu.add_command(label='Long entry that does nothing')
        labels = ['A', 'B', 'C', 'D', 'E', 'F']
        for item in labels:
            bmenu.add_command(label='Print letter "{}"'.format(item),
                              underline=14,
                              accelerator='Control+{}'.format(item),
                              command=lambda i=item: self._print_it(None, i))
             
            # bind accelerator key to a method; the bind is on ALL the
            # applications widgets
            self.bind_all('<Control-{}>'.format(item.lower()),
                            lambda e, i=item: self._print_it(e, i))
 
    # Cascades menu ------------------------------------------------------------------           
    def _add_cascades_menu(self):
        cascades = Menu(self._menu)
        self._menu.add_cascade(label='Cascades', menu=cascades, underline=0)
         
        cascades.add_command(label='Print Hello', underline=6,accelerator='Control+H',command=lambda: self._print_it(None, 'Hello'))
 
        cascades.add_command(label='Print Goodbye', underline=6,accelerator='Control+G',command=lambda: self._print_it(None, 'Goodbye'))
 
        # add submenus       
        self._add_casc_cbs(cascades)    # check buttons
        self._add_casc_rbs(cascades)    # radio buttons
 
        # bind accelerator key to a method; the bind is on ALL the
        # applications widgets
        self.bind_all('<Control-h>',
                        lambda e: self._print_it(e, 'Hello'))
        self.bind_all('<Control-g>',
                        lambda e: self._print_it(e, 'Goodbye'))
 
    def _add_casc_cbs(self, cascades):
        # build the Cascades->Check Buttons submenu
        check = Menu(cascades)
        cascades.add_cascade(label='Check Buttons', underline=0,menu=check)
         
        self.__vars = {}
        labels = ('Oil checked', 'Transmission checked','Brakes checked', 'Lights checked' )
 
        for item in labels:
            self.__vars[item] = IntVar()
            check.add_checkbutton(label=item, variable=self.__vars[item])
             
        # set items 1 and 3 to 'selected' state
        check.invoke(1)
        check.invoke(3)
             
        check.add_separator()
        check.add_command(label='Show values',
                          command=lambda lbls=labels: self._show_vars(lbls))
                     
    def _add_casc_rbs(self, cascades):
        # build Cascades->Radio Buttuns subment
        submenu = Menu(cascades)
        cascades.add_cascade(label='Radio Buttons', underline=0,menu=submenu)
         
        self.__vars['size'] = StringVar()
        self.__vars['font'] = StringVar()
         
        for item in (10,14,18,24,32):
            submenu.add_radiobutton(label='{} points'.format(item),variable=self.__vars['size'])
             
        submenu.add_separator()
        for item in ('Roman', 'Bold', 'Italic'):
            submenu.add_radiobutton(label=item,variable=self.__vars['font'])
     
        # set items 1 and 7 to 'selected' state
        submenu.invoke(1)
        submenu.invoke(7)
             
        submenu.add_separator()
        submenu.add_command(label='Show values',command=lambda: self._show_vars(('size','font')))     
     
    # More menu ------------------------------------------------------------------   
    def _add_more_menu(self):
        menu = Menu(self._menu)
        self._menu.add_cascade(label='More', menu=menu, underline=0)
         
        labels = ('An entry', 'Another entry', 'Does nothing','Does almost nothing', 'Make life meaningful')
         
        for item in labels:
            menu.add_command(label=item,
                             command=lambda i=item: self._you_invoked((i, 'entry')))
             
        menu.entryconfig(3, bitmap='questhead', compound=LEFT,
                         command=lambda i=labels[3]:
                                    self._you_invoked((i,
                                                      'entry; a bitmap and a text string')))           
           
    # Colors menu ------------------------------------------------------------------          
    def _add_colors_menu(self):
        menu = Menu(self._menu, tearoff=True)
        self._menu.add_cascade(label='Colors', menu=menu, underline=1)
         
        for c in ('red', 'orange', 'yellow', 'green', 'blue'):
            menu.add_command(label=c, background=c,
                             command=lambda c=c: self._you_invoked((c, 'color')))   
            
    
    
    #Carga una imagen deseada, crea una mariposa, la muestra, pregunta si esta rota y la guarda en la bd
    def load_but(self):
        b = str(askopenfile())
        path = get_path(b)
        i = np.array(Image.open(path))
        #Creamos la mariposa
        name = 'ima/' + os.path.basename(path)
        self.but_act = butterfly(i,name)
        
        s = tkMessageBox.askquestion("Integridad", "Le falta algun trozo al ejemplar?")        
        self.but_act.set_broken(s)
        self._create_widgets(i)
        if self.db.new_but(self.but_act) == -1:
            self.refresh_grid()
            tkMessageBox.showinfo(None, "La mariposa ya esta en la base de datos o se ha producido un error")
        else:
            tkMessageBox.showinfo(None, "La mariposa ha sido aniadida a la base de datos, aunque todavia no pa sido procesada.")
        #self.w.mainloop()
        
    def new_col(self):
        '''TODO'''
        self.dialog_col()
    
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
        
                     
    # ================================================================================
    # Bound and Command methods
    # ================================================================================               
    def _print_it(self, e, txt):
        # triggered by multiple menu items that print letters or greetings
        # or by an accelerator keypress (Ctrl+a, Ctrl+b, etc).
        print(txt)       
         
    def _update_status(self, evt):
        # triggered on mouse entry if a menu item has focus
        # (focus occurs when user clicks on a top level menu item)
        '''try:
            item = self.tk.eval('%s entrycget active -label' % evt.widget )
            self.__status.configure(background='gray90', foreground='black',
                                    text=item)
        except TclError:
            # no label available, ignore
            pass'''
         
    def _show_vars(self, values):
        # called when Cascades->Check Buttons or Radio Buttons
        # 'Show Values' item is selected
        # displayf variable values in the status bar
        v = []
        for e in values:
            t = self.__vars[e].get()
            s = '{}: {}  '.format(e, t)
            v.append(s)
         
        self.__status.configure(background='white', foreground='black',
                                text=''.join(v))
     
    def _you_invoked(self, value):
        # triggered when an entry in the Icons, More or Colors menu is selected
        self.bell()
        self.__status.configure(background='SeaGreen1', foreground='black', text="You invoked the '{}' {}.".format(value[0],value[1]))
                
    class dialog_col:
        root = None
        e1 = None
        img = Null
        
        def __init__(self):
            self.root = Tk()
            frame = Frame(self.root,name='dialog_col')
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
            
                   
#Par de bucles para extraer la ruta de la imagen que hemos seleccionado en el explorador
def get_path(s):
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
         
if __name__ == '__main__':
    MenuDemo().mainloop()