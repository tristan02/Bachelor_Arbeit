'''
Created on 24/3/2015

@author: Psilocibino
'''
from Tkinter import *
import ttk
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
from _warnings import default_action
import ScrolledText

 
class MenuDemo(ttk.Frame):
    
    w = Null
    but_act = Null
    frame = Null
    panel = Null
    grid = Null
    img = Null
    btn_act_but = Null
    btn_act_col = Null
    db = None
    _instance_new_col = None
    _instance_but_act = None
    new_col = None
    e1 = None
    img = Null
    Colecciones = None
    btn_cols = {}
    col_act = '-'
    estudio = False
     
    def __init__(self, name='menu'):        
        ttk.Frame.__init__(self, name=name)
        self.pack(fill=BOTH)
        self.master.title('Buterflies Database')
        self.db = database()
        im = Image.open('no-image.png')
        self.no_img = ImageTk.PhotoImage(im)
        self._create_panel()        
    
    def _create_panel(self):
        Panel = Frame(self, name='panel')
        Panel.pack(side=TOP, fill=BOTH)
         
        msg = ["Butterflies Database"]
         
        lbl = Label(Panel, text=''.join(msg), wraplength='4i', justify=LEFT)
        lbl.pack(side=TOP, padx=5, pady=5)
        
        #Frame para opciones
        Tareas = Frame(name='tareas',padx=20,pady=20)
        Tareas.pack()
        #Button collection
        im = Image.open('upload.jpg')
        imh = ImageTk.PhotoImage(im)
        btn_new_col = Button(Tareas,text='New Collection...', image=imh, default=ACTIVE, command=self.new_col)
        btn_new_col.image = imh
        btn_new_col['compound'] = LEFT
        btn_new_col.focus()
        btn_new_col.pack(side=LEFT)        
        #Button nueva mariposa
        im = Image.open('new.png')
        imh = ImageTk.PhotoImage(im)
        btn_new_but = Button(Tareas,name='btn_new_but', text='New Butterfly...', image=imh, default=ACTIVE, command=self.load_but)
        btn_new_but.image = imh
        btn_new_but['compound'] = LEFT
        btn_new_but.focus()
        btn_new_but.pack(side=RIGHT)
        
        #Frame para mariposa actual
        Central = Frame(name='panel central')
        Central.pack()        
        self.btn_act_but = Button(Central,name='btn_act_but', image=self.no_img, default=ACTIVE, command=self.edit_but)
        self.btn_act_but.image = imh
        self.btn_act_but.focus()
        #self.btn_act_but.pack(side=BOTTOM)
        
        im = Image.open('next.png')
        imn = ImageTk.PhotoImage(im)
        self.btn_next_but = Button(Central,name='btn_next_but', image=imn, default=ACTIVE, command=self.next_but)
        self.btn_next_but.image = imn
        self.btn_next_but.focus()
        #self.btn_next_but.pack(side= RIGHT)
        
        im = Image.open('prev.png')
        imn = ImageTk.PhotoImage(im)
        self.btn_prev_but = Button(Central,name='btn_prev_but', image=imn, default=ACTIVE, command=self.prev_but)
        self.btn_prev_but.image = imn
        self.btn_prev_but.focus()
        #self.btn_prev_but.pack(side= LEFT)
        
        self.btn_prev_but.grid(row=0, column=1)
        self.btn_act_but.grid(row=0, column=2)
        self.btn_next_but.grid(row=0, column=3)
        
        #Frame para seleccion de coleciones existenetes
        self.Colecciones = Frame(name='colecciones')
        self.Colecciones.pack()
        tit = 'Colecciones disponibles:'
        tit_cols = Label(self.Colecciones, text=''.join(tit), wraplength='4i')
        tit_cols.pack(side=TOP, padx=5, pady=5)  
        for i in self.db.get_cols():
            action = lambda x = i: self.set_col(x)
            self.btn_cols[i] = Button(self.Colecciones, text=i, width=20,command=action) 
            self.btn_cols[i].pack()
        self.col_act = '-'
        
        #Frame para la coleccion actual
        self.Coleccion = Frame(name='coleccion_actual')
        self.Coleccion.pack()
        self.btn_act_col = Button(self.Coleccion,name='btn_act_col', width=20, text='Coleccion actual: '+self.col_act, default=ACTIVE, command=self.show_info_col)
        self.btn_act_col.focus()
        self.btn_act_col.pack(side=BOTTOM,padx=25, pady=25)
        
                 
        # create statusbar
        statusBar = Frame()
        self.__status = Label(self.master, text=' ', borderwidth=1,font=('Helv 10'), name='status')
         
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
        self._add_collection_menu()
        #self._add_colors_menu()
 
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
    def _add_collection_menu(self):
        collection = Menu(self._menu)
        self._menu.add_cascade(label='Collection', menu=collection, underline=0)
         
        collection.add_command(label='Print Hello', underline=6,accelerator='Control+H',command=lambda: self._print_it(None, 'Hello'))
 
        collection.add_command(label='Print Goodbye', underline=6,accelerator='Control+G',command=lambda: self._print_it(None, 'Goodbye'))
 
        # add submenus       
        self._add_casc_but(collection)    # check buttons
        self._add_casc_rbs(collection)    # radio buttons
 
        # bind accelerator key to a method; the bind is on ALL the
        # applications widgets
        self.bind_all('<Control-h>',
                        lambda e: self._print_it(e, 'Hello'))
        self.bind_all('<Control-g>',
                        lambda e: self._print_it(e, 'Goodbye'))
 
    def _add_casc_but(self, cascades):
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
        check.add_command(label='Show values',command=lambda lbls=labels: self._show_vars(lbls))
        
    def _refresh_casc_cbs(self, cascades):
        cascades.entryconfigure(1,'Bieeen')
                     
    def _add_casc_rbs(self, cascades):
        # build Cascades->Radio Buttuns subment
        submenu = Menu(cascades)
        cascades.add_cascade(label='Radio Buttons', underline=0,menu=submenu)
         
        self.__vars['size'] = StringVar()
        self.__vars['font'] = StringVar()
         
        for item in (10,14,18,24,32):
            submenu.add_radiobutton(label='{} points'.format(item),variable=self.__vars['size'])
             
        submenu.add_separator()
        '''TODO'''
        conj = self.db.get_cols()
        for i in conj:
            donothing_callback()
        for item in conj:
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
                             command=lambda i=item: self._you_invoked((i,'entry')))
             
        menu.entryconfig(3, bitmap='questhead', compound=LEFT,command=lambda i=labels[3]:self._you_invoked((i,'entry; a bitmap and a text string')))           
           
    # Colors menu ------------------------------------------------------------------          
    def _add_colors_menu(self):
        menu = Menu(self._menu, tearoff=True)
        self._menu.add_cascade(label='Colors', menu=menu, underline=1)
         
        for c in ('red', 'orange', 'yellow', 'green', 'blue'):
            menu.add_command(label=c, background=c,command=lambda c=c: self._you_invoked((c, 'color')))   
            
    def reset_btn_act_but(self):
        im = Image.open('no-image.png')
        imh = ImageTk.PhotoImage(im)
        self.btn_act_but.config(image=imh)
        
    def set_col(self,col): 
        self.col_act = col
        self.btn_act_col.config(text='Coleccion actual: '+self.col_act,bg = "firebrick3")
        if not(self.estudio):
            self.show_buts(self.db.get_buts_col(col))
        
    def update_cols(self,n):        
        btn_new_col = Button(self.Colecciones,name=n.lower(),text=n,default=ACTIVE, width=20, command=lambda:self.set_col(n))
        btn_new_col.pack()
        self.Colecciones.pack()
        self.set_col(n)
        '''TODO
        self._add_collection_menu()'''
    
    #Carga una imagen deseada, crea una mariposa, la muestra, pregunta si esta rota y la guarda en la bd
    def load_but(self):
        if not(self.estudio):
            self.estudio = True
            b = str(askopenfile())
            path = get_path(b)
            i = np.array(Image.open(path))
            #Creamos la mariposa
            name = 'ima/' + os.path.basename(path)
            self.but_act = butterfly(i,name)
            
            s = tkMessageBox.askquestion("Integridad", "Le falta algun trozo al ejemplar?")        
            self.but_act.set_broken(s)
            self.update_frame_new_but(self.but_act.get_min_img())
            if self.db.new_but(self.but_act) == -1:
                tkMessageBox.showinfo(None, "La mariposa ya esta en la base de datos o se ha producido un error")
            else:
                tkMessageBox.showinfo(None, "La mariposa ha sido aniadida a la base de datos, pero sin procesar.")
        else:
            s = tkMessageBox.askquestion(None, "Existe una mariposa pendiente de estudio. Desea descartarla?")
            if s == 'yes':
                self.delete_but()
      
        
    def edit_but(self):
        if self.col_act != '-':
            if not(self.but_act == Null):
                if self._instance_but_act == None:
                    self.dialog_edit_but()
            else:
                tkMessageBox.showinfo(None, "Ninguna mariposa para procesar")
        else:
            tkMessageBox.showinfo(None, "Seleccione primero una coleccion, o cargue una mariposa nueva!")
        
    def new_col(self):
        if self._instance_new_col == None:
            self.dialog_new_col()
            '''self.update_cols()'''
            
    def show_info_col(self):
        (info,img) = self.db.get_info_col(self.col_act)
        tkMessageBox._show(self.col_act, info)
        
    def close_but(self):
        if self.panel != Null:
            self.panel.destroy()
        self.frame.destroy()
        self.db.delete_db()       
        
    def show_buts(self,buts):
        if buts != []:
            self.buts = buts
            self.but_act = self.buts[0] 
            self.update_frame_but(buts[0].get_min_img())
            self.index_but_act = 0 
            self.count_buts = len(buts)-1
        else:
            self.buts = buts
            self.update_frame_but(buts)
            self.index_but_act = 0 
            self.count_buts = 0
        
    def next_but(self):
        if not(self.estudio) and self.but_act != Null:
            if self.index_but_act != self.count_buts:
                self.index_but_act = self.index_but_act + 1
            else:
                self.index_but_act = 0
            
            self.but_act = self.buts[self.index_but_act]     
            self.update_frame_but(self.buts[self.index_but_act].get_min_img())
        
    def prev_but(self):
        if not(self.estudio) and self.but_act != Null:
            if self.index_but_act != 0:
                self.index_but_act = self.index_but_act - 1
            else:
                self.index_but_act = self.count_buts
            self.but_act = self.buts[self.index_but_act] 
            self.update_frame_but(self.buts[self.index_but_act].get_min_img())
        
    def show_masks(self):        
        c = self.db.get_count_but()
        for i in range(c):
            but = self.db.get_but(i)
            cv2.imshow(but.get_name(), but.get_mask())
     
    #De momento abrimos una ventana con el histograma de cada mariposa       
    def show_hist(self):
        '''TODO'''
        c = self.db.get_count_but()
        for i in range(c):
            but = self.db.get_but(i)
            cv2.imshow(but.get_name(), but.get_hist())
        MenuDemo._instance_but_act = None
        self.root.destroy()
    
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
        #self.refresh_grid()
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
            
    def update_frame_new_but(self,img):
        self.btn_act_but.config(image=img,text='Mariposa pendiente de estudio')          
        self.btn_act_but['compound'] = BOTTOM  
        
    def update_frame_but(self,but):
        if but != []:
            self.btn_act_but.config(image=but)   
        else:
            self.btn_act_but.config(image=self.no_img)
        if not(self.estudio):
            self.btn_act_but.config(text='')
        
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
        
    #Funcion para el dialogo para crear una nueva coleccion. Tenemos la opcion de subir tambien una foto que se guardara en el objeto collecion
    def dialog_new_col(self):
        self.new_col = Tk()
        frame = Frame(self.new_col,name='dialog_new_col', width=200, height=200)
        self.new_col.title('Nueva coleccion...')
        frame.pack()
    
        label1 = Label(frame, text="Nombre de la nueva coleccion:",padx=20,pady=20) 
        self.e1 = Entry(frame, bd =5)
        label2 = Label(frame, text="Informacion adicional:",padx=10,pady=10) 
        self.e2 = ScrolledText.ScrolledText(frame,width=40, height=5, wrap=WORD,padx=10,pady=10)
        self.subir_foto = Button(frame, text="Subir foto...", command=self.foto_col) 
        self.crear = Button(frame, text="Crear", command=self.crear)
        
        label1.pack(side=LEFT)
        label2.pack(side=LEFT)
        self.e1.pack(side = RIGHT)
        self.e2.pack(side = RIGHT)
        self.subir_foto.pack(side=LEFT) 
        self.crear.pack(side=RIGHT)
        
        label1.grid(row=0, column=0)
        self.e1.grid(row=0, column=1)
        label2.grid(row=1, column=0)
        self.e2.grid(row=1, column=1)
        self.subir_foto.grid(row=2, column=0)
        self.crear.grid(row=2, column=1)
        
        self._instance_new_col = self
            
        self.new_col.mainloop() 
        
    def crear(self):        
        nom = self.e1.get()
        inf = self.e2.get(1.0, END)
        col = collection(self.img,nom,inf)
        self.db.new_col(col)
        self._instance_new_col = None
        self.update_cols(nom)
        self.new_col.destroy() 
        self.new_col = None
        
    def foto_col(self):
        f = str(askopenfile())
        path = get_path(f)
        self.img = np.array(Image.open(path))
        
        

    def dialog_edit_but(self):
        self.root = Tk()
        frame = Frame(self.root,name='dialog_edit',padx=20,pady=20)
        self.root.title('Editar...')
        frame.pack()
        
        label = Label(frame, text="Opciones:")
        if self.estudio:        
            self.ins_but = Button(frame, text="Insertar en base de datos", width=25, command=self.comparar)
            self.sh_hist = Button(frame, text="Mostrar histograma", width=25, command=self.show_hist)
            self.del_but = Button(frame, text="Descartar mariposa", width=25, command=self.delete_but) 
                       
            label.grid(row=0, column=0)        
            self.ins_but.grid(row=1, column=0)
            self.sh_hist.grid(row=2, column=0)
            self.del_but.grid(row=3, column=0)
        else:
            self.buts_col = Button(frame, text="Mostrar mariposas de color parecido", width=35, command=self.comparar)
            self.buts_shape = Button(frame, text="Mostrar mariposas de forma parecida", width=35, command=self.comparar)
            self.sh_hist = Button(frame, text="Mostrar histograma", width=35, command=self.show_hist)
            self.del_but = Button(frame, text="Eliminar mariposa", width=35, command=self.delete_but) 
                       
            label.grid(row=0, column=0)        
            self.buts_col.grid(row=1, column=0)
            self.buts_shape.grid(row=2, column=0)
            self.sh_hist.grid(row=3, column=0)
            self.del_but.grid(row=4, column=0)
        
        MenuDemo._instance_but_act = self
            
        self.root.mainloop()   
        
    def delete_but(self):
        s = tkMessageBox.askquestion(None, "Esta seguro que quiere eliminar permanentemente este ejemplar?")
        if s == 'yes':
            if not(self.estudio):
                self.db.del_item(self.but_act)                
            self.but_act = Null
            self.update_frame_but(self.no_img)
            self._instance_but_act = None
            self.estudio = False
            self.root.destroy()
                            
    def comparar(self):
        '''TODO'''
        MenuDemo._instance_but_act = None
        self.root.destroy()
                      
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