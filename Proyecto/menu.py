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
import ScrolledText
from Proyecto.get_histogram import compare_hist

 
class MenuDemo(ttk.Frame):    
    but_act = Null
    col_act = '-'
    panel = Null
    img = Null
    btn_act_but = Null
    btn_act_col = Null
    db = None
    _instance_new_col = None
    _instance_but_act = None
    new_col = None
    img = Null
    Colecciones = None
    btn_cols = {}    
    estudio = False
    dist03 = 0
    index_but_act = 0
    count_buts = 0
    name_but_act = ''
    x_d0 = -1
    x_d3 = -1
    count_click = 0
     
    def __init__(self, name='menu'):        
        ttk.Frame.__init__(self, name=name)
        self.pack(fill=BOTH)
        self.master.title('Buterflies Database')
        self.db = database()
        im = Image.open('no-image.png')
        self.no_img = ImageTk.PhotoImage(im)
        self._create_panel()         
        if self.db.get_col_act() != '-':
            self.set_col(self.db.get_col_act())
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    
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
        
        self.lb_name_but = Label(Central, text=str(self.name_but_act), wraplength='4i')
                
        self.btn_act_but = Button(Central,name='btn_act_but', image=self.no_img, default=ACTIVE, command=self.edit_but)
        self.btn_act_but.image = imh
        self.btn_act_but.focus()
        
        im = Image.open('next.png')
        imn = ImageTk.PhotoImage(im)
        self.btn_next_but = Button(Central,name='btn_next_but', image=imn, default=ACTIVE, command=self.next_but)
        self.btn_next_but.image = imn
        self.btn_next_but.focus()
        
        im = Image.open('prev.png')
        imn = ImageTk.PhotoImage(im)
        self.btn_prev_but = Button(Central,name='btn_prev_but', image=imn, default=ACTIVE, command=self.prev_but)
        self.btn_prev_but.image = imn
        self.btn_prev_but.focus()
        
        self.lb_num_but = Label(Central, text=str(self.index_but_act) +' de '+ str(self.count_buts), wraplength='4i')
        
        self.lb_name_but.grid(row=0,column=2)
        self.btn_prev_but.grid(row=1, column=1)
        self.btn_act_but.grid(row=1, column=2)
        self.btn_next_but.grid(row=1, column=3)
        self.lb_num_but.grid(row=2, column=2)
        
        #Frame para la coleccion actual
        self.Coleccion = Frame(name='coleccion_actual')
        self.Coleccion.pack()
        self.btn_act_col = Button(self.Coleccion,name='btn_act_col', width=20, text='Coleccion actual: '+self.col_act, default=ACTIVE, command=self.dialog_edit_col)
        self.btn_act_col.focus()
        self.btn_act_col.pack(side=BOTTOM,padx=25, pady=25)
        
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
        
        # create statusbar
        statusBar = Frame()
        self.__status = Label(self.master, text=' ', borderwidth=1,font=('Helv 10'), name='status')
         
        self.__status.pack(side=LEFT, padx=2, fill=BOTH)
        statusBar.pack(side=BOTTOM, fill=X, pady=2)
                 
        # create the main menu (only displays if child of the 'root' window)
        self.master.option_add('*tearOff', False)  # disable all tearoff's
        self._menu = Menu(self.master, name='menu')
        self.master.config(menu=self._menu)
         
        self._add_file_menu()
 
 
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
        filemenu.add_command(label='Exit', command=self.on_closing) # kill toplevel wnd
        
    
    # ================================================================================
         
       
            
    def reset_btn_act_but(self):
        im = Image.open('no-image.png')
        imh = ImageTk.PhotoImage(im)
        self.btn_act_but.config(image=imh)
        
    #Establece como coleccion actual la que viene pasada por parametro. El boton rojo se actualiza. En caso de que estemos
    #estudiando un especimen nuevo, nos preguntara si queremos descartar dicho item.
    def set_col(self,col): 
        self.col_act = col
        self.btn_act_col.config(text='Coleccion actual: '+self.col_act,bg = "firebrick3",fg='white')
        if not(self.estudio):
            self.show_buts(self.db.get_buts_col(col))
    
    #Una vez creada una nueva coleccion, creamos un nuevo boton con el nombre de la nueva coleccion.    
    def update_cols(self,n): 
        self.btn_cols[n] = Button(self.Colecciones,name=n.lower(),text=n,default=ACTIVE, width=20, command=lambda:self.set_col(n))      
        self.btn_cols[n].pack()
        self.Colecciones.pack()
        self.set_col(n)
        '''TODO
        self._add_collection_menu()'''
    
    #Carga una imagen deseada, crea una mariposa, la muestra, pregunta si esta rota y la guarda en la bd
    def load_but(self):
        if not(self.estudio):            
            try:
                self.estudio = True
                b = str(askopenfile())
                path = get_path(b)
                i = np.array(Image.open(path))
                #Creamos la mariposa
                name = 'ima/' + os.path.basename(path)
                self.but_act = butterfly(i,name)
                #Preguntamos al usuario si sobre la integridad del ejemplar
                s = tkMessageBox.askquestion("Integridad", "Le falta algun trozo al ejemplar?")        
                self.but_act.set_broken(s)
                self.update_frame_new_but(self.but_act.get_min_img())
                '''if self.db.new_but(self.but_act) == -1:
                    tkMessageBox.showinfo(None, "La mariposa ya esta en la base de datos o se ha producido un error")
                else:
                    tkMessageBox.showinfo(None, "La mariposa ha sido aniadida a la base de datos, pero sin procesar.")'''
            except:
                self.estudio = False
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
            tkMessageBox.showinfo(None, "Seleccione primero una coleccion, o cree una nueva!")
        
    def new_col(self):
        if self._instance_new_col == None:
            self.dialog_new_col()
            
    def show_info_col(self):
        '''TODO: Opciones para eliminar/editar una coleccion a parte de mostrar informacion etc'''
        self.win_edit_col.destroy()
        if not(self.col_act == '-'):
            (info,img) = self.db.get_info_col(self.col_act)
            tkMessageBox._show(self.col_act, info)
        else:
            tkMessageBox.showinfo('None', 'Ninguna coleccion para cargar. Cree una.')
    def close_but(self):
        if self.panel != Null:
            self.panel.destroy()
        self.frame.destroy()
        self.db.delete_db()       
        
    def show_buts(self,buts):
        if buts != []:
            self.num_but_act = 1
            self.buts = buts
            self.but_act = self.buts[0] 
            self.update_frame_but(buts[0].get_min_img())
            self.index_but_act = 0 
            self.count_buts = len(buts)-1
            self.lb_num_but.config(text=str(self.index_but_act+1) +' de  '+ str(self.count_buts+1))
            self.lb_name_but.config(text=self.but_act.get_name())
        else:
            self.but_act = Null
            self.buts = buts
            self.update_frame_but(buts)
            self.index_but_act = 0 
            self.count_buts = 0
            self.lb_num_but.config(text='0 de 0')
            self.lb_name_but.config(text='')
        
    def next_but(self):
        if not(self.estudio) and self.but_act != Null:
            try:
                if self.index_but_act != self.count_buts:
                    self.index_but_act = self.index_but_act + 1
                else:
                    self.index_but_act = 0
                       
                self.lb_num_but.config(text=str(self.index_but_act+1) +' de  '+ str(self.count_buts+1))
                self.but_act = self.buts[self.index_but_act]  
                print str(self.but_act.get_dist03()) 
                self.update_frame_but(self.buts[self.index_but_act].get_min_img())
                self.lb_name_but.config(text=self.but_act.get_name())
            except TclError:
                pass 
        
    def prev_but(self):
        if not(self.estudio) and self.but_act != Null:
            try:
                if self.index_but_act != 0:
                    self.index_but_act = self.index_but_act - 1
                else:
                    self.index_but_act = self.count_buts
                self.lb_num_but.config(text=str(self.index_but_act+1) +' de  '+ str(self.count_buts+1))                
                self.but_act = self.buts[self.index_but_act] 
                self.update_frame_but(self.buts[self.index_but_act].get_min_img())
                self.lb_name_but.config(text=self.but_act.get_name())
            except TclError:
                pass 
        
    def show_masks(self):        
        c = self.db.get_count_but()
        for i in range(c):
            but = self.db.get_but(i)
            cv2.imshow(but.get_name(), but.get_mask())
     
    #De momento abrimos una ventana con el histograma de cada mariposa       
    def show_hist(self):
        cv2.imshow(self.but_act.get_name(), self.but_act.get_hist_img())
        MenuDemo._instance_but_act = None
        self.win_new_but.destroy()
    
    'TODO: El reescalado se debe hacer en la base de datos al aniadir nueva mariposa Este metodo sobra'
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
                ''''TODO Si no se ha detectado bien el 03 hay que hacer algo!'''
                #self.db.delete_but(but)
                error = error + 1
        d = d/(c-error)
        self.db.reescale_bd(d)
        
    def get_dist03_but(self):
        self.dist03,img_03 = find_0_3(self.but_act.get_np_img())
        
        im = Image.fromarray(img_03)
        imh = ImageTk.PhotoImage(im)
        
        self.win_dist03 = Toplevel()
        #self.win_dist03.protoco("WM_DELETE_WINDOW", "onexit")
        fr_dist03_img = Frame(self.win_dist03)
        self.fr_dist03_dialog = Frame(self.win_dist03)
              
        fr_dist03_img.pack(side = BOTTOM)
        self.fr_dist03_dialog.pack(side = TOP)
        
        lbl_img_dist03 = Label(fr_dist03_img, image=imh)
        lbl_img_dist03.image = imh
        lbl_img_dist03.bind("<Button-1>", self.callback)
        lbl_img_dist03.pack(side = "bottom", fill = "both", expand = "yes")
        
        lbl_description_dist03 = Label(self.fr_dist03_dialog, text='Deberian verse dos puntos azules. Uno en el 0 y otro en el 3 de la regla.')
        lbl_description_dist03.grid(row=0)
        
        btn_yes_dist03 = Button(self.fr_dist03_dialog, name='btn_yes_dist03', text = 'Se muestran correctamente',bg = "green", default=ACTIVE, command=self.good_dist03)
        btn_no_dist03 = Button(self.fr_dist03_dialog, name='btn_no_dist03', text = 'No se muestran correctamente',bg = "red", command=self.bad_dist03)
        btn_yes_dist03.grid(row=1, column=0)
        btn_no_dist03.grid(row=1, column=1)
        
        '''TODO: Recolocar botones y mensaje. Dejarlo bonito'''
        
    def good_dist03(self):
        self.win_dist03.destroy()
        self.but_act.set_dist03(self.dist03)
   
    def bad_dist03(self):
        self.fr_dist03_dialog.destroy()
        fr_dist03_correct = Frame(self.win_dist03)
        fr_dist03_correct.pack(side = BOTTOM)
        labelfont = ('times', 20, 'bold')
        lbl_correct_dist03 = Label(fr_dist03_correct,font=labelfont, text = 'Haga CLICK primero en el CERO y duespues en el TRES.',fg='red')
        lbl_correct_dist03.pack()
         
    def callback(self,event):
        if self.count_click == 0:
            self.x_d0 = event.x
            self.count_click = self.count_click + 1
        elif self.count_click == 1:
            self.x_d3 = event.x
            self.dist03 = self.x_d3 - self.x_d0
            self.but_act.set_dist03(self.dist03)  
            self.win_dist03.destroy()
            self.count_click = 0 
            self.x_d0 = -1
            self.x_d3 = -1 
            print str(self.dist03)  
    
    #Actualiza la imagen del frame central al insertar nueva mariposa.       
    def update_frame_new_but(self,img):
        self.btn_act_but.config(image=img,fg='red', text='Mariposa pendiente de estudio')          
        self.btn_act_but['compound'] = BOTTOM
        self.lb_name_but.config(text='')
        self.lb_num_but.config(text='0 de 0')
    
    #Cambia del tiron a la coleccion y a la mariposa que le pasamos como argumento 
    def set_frame_central(self,but): 
        self.win_similar_buts.destroy()
        col,index = self.db.get_col_from_but(but)
        self.set_col(col)
        self.show_buts(self.db.get_buts_col(col))
        for i in range(index):
            self.next_but()
    
    #Actualizamos el frame central con una nueva imagen y quitamos la etqiqueta 'en estudio' en caso de que ya no sea precisa    
    def update_frame_but(self,img):
        if img != []:
            self.btn_act_but.config(image=img)   
        else:
            self.btn_act_but.config(image=self.no_img)
        if not(self.estudio):
            self.btn_act_but.config(text='')
    
    #Carga una nueva base de datos a partir de un archivo de texto    
    def load_db(self):
        b = str(askopenfile())
        path = self.get_path(b)
        self.db.load_db(path)       
        
    #==============================================================================================================
    #FUNCIONES DE DIALOGOS
    #==============================================================================================================
        
    
    #Funcion para el dialogo para crear una nueva coleccion. Tenemos la opcion de subir tambien una foto que se guardara en el objeto collecion
    def dialog_new_col(self):
        self.win_new_col = Toplevel()
        self.win_new_col.protocol("WM_DELETE_WINDOW", "onexit")
        frame = Frame(self.win_new_col,name='dialog_new_col', width=200, height=200)
        self.win_new_col.title('Nueva coleccion...')
        frame.pack()
    
        label1 = Label(frame, text="Nombre de la nueva coleccion:",padx=20,pady=20) 
        self.e1 = Entry(frame, bd =5)
        label2 = Label(frame, text="Informacion adicional:",padx=10,pady=10) 
        self.e2 = ScrolledText.ScrolledText(frame,width=40, height=5, wrap=WORD,padx=10,pady=10)
        self.subir_foto = Button(frame, text="Subir foto...", command=self.foto_col) 
        self.crear = Button(frame, text="Crear", command=self.crear_col)
           
        label1.grid(row=0, column=0)
        self.e1.grid(row=0, column=1)
        label2.grid(row=1, column=0)
        self.e2.grid(row=1, column=1)
        self.subir_foto.grid(row=2, column=0)
        self.crear.grid(row=2, column=1)
        
        self._instance_new_col = self
            
        self.win_new_col.mainloop() 
        
    def crear_col(self):        
        nom = self.e1.get()
        inf = self.e2.get(1.0, END)
        col = collection(self.img,nom,inf)
        self.db.new_col(col)
        self._instance_new_col = None
        self.update_cols(nom)
        self.win_new_col.destroy() 
        self.win_new_col = None
        self.lb_name_but.config(text='')
        
    def foto_col(self):
        f = str(askopenfile())
        path = get_path(f)
        self.img = np.array(Image.open(path))    
        
        
    def dialog_edit_col(self):
        self.win_edit_col= Toplevel()
        self.frame_options_col = Frame(self.win_edit_col,padx=20,pady=20)
        self.win_edit_col.title('Editar coleccion...')
        self.frame_options_col.pack()
        
        self.ins_but = Button(self.frame_options_col, text="Descripcion", width=25, command=self.show_info_col)
        self.sh_hist = Button(self.frame_options_col, text="Renombrar coleccion", width=25, command=self.rename_col)
        self.del_but = Button(self.frame_options_col, text="Eliminar coleccion", width=25, command=self.delete_col) 
         
        lb_opc = Label(self.frame_options_col, text="Opciones:")           
        lb_opc.grid(row=0, column=0)        
        self.ins_but.grid(row=1, column=0)
        self.sh_hist.grid(row=2, column=0)
        self.del_but.grid(row=3, column=0)
        
    def delete_col(self):
        self.win_edit_col.destroy()
        if self.db.get_buts_col(self.col_act) != []:
            s = tkMessageBox.askquestion(None, "Esta seguro que quiere eliminar permanentemente esta coleccion con todas las mariposas que contiene?")
            if s == 'yes':
                self.db.del_col(self.col_act)
                self.btn_cols[self.col_act].destroy()
                self.set_col('')
        else:
            self.db.del_col(self.col_act)
            self.btn_cols[self.col_act].destroy()
            self.set_col('')
            
    def rename_col(self):
        self.win_rename_col = Toplevel()
        fr_rename_col = Frame(self.win_rename_col,padx=20,pady=20)
        self.win_rename_col.title('Renombrar coleccion...')
        fr_rename_col.pack()
        
        self.win_edit_col.destroy()
        
        lb_rename_col = Label(fr_rename_col, text='Nuevo nombre:  ')
        self.ent_rename_col = Entry(fr_rename_col, bd =5)
        btn_rename_col = Button(fr_rename_col, text='OK', width=10, command=self.rename_col_event)
        
        lb_rename_col.grid(row=0, column=0)        
        self.ent_rename_col.grid(row=0, column=1)
        btn_rename_col.grid(row=0, column=2)
        
    def rename_col_event(self):
        n_name = self.ent_rename_col.get()
        self.win_rename_col.destroy()
        self.db.rename_col(self.col_act,n_name)           
        self.btn_cols[self.col_act].destroy()   
        action = lambda x = n_name: self.set_col(x)    
        self.btn_cols[n_name] = Button(self.Colecciones, text=n_name, width=20,command=action) 
        self.btn_cols[n_name].pack()        
        self.set_col(n_name)
    
    def dialog_edit_but(self):
        self.win_new_but = Toplevel()
        self.win_new_but.protocol("WM_DELETE_WINDOW", "onexit")
        self.frame_options_but = Frame(self.win_new_but,name='dialog_edit',padx=20,pady=20)
        self.win_new_but.title('Editar mariposa...')
        self.frame_options_but.pack()
        
        lb_opc = Label(self.frame_options_but, text="Opciones:")
        if self.estudio:        
            self.ins_but = Button(self.frame_options_but, text="Insertar en base de datos", width=25, command=self.insert_but)
            self.sh_hist = Button(self.frame_options_but, text="Mostrar histograma", width=25, command=self.show_hist)
            self.del_but = Button(self.frame_options_but, text="Descartar mariposa", width=25, command=self.delete_but) 
                       
            lb_opc.grid(row=0, column=0)        
            self.ins_but.grid(row=1, column=0)
            self.sh_hist.grid(row=2, column=0)
            self.del_but.grid(row=3, column=0)
        else:
            self.buts_col = Button(self.frame_options_but, text="Mostrar mariposas de color parecido", width=35, command=self.comp_color)
            self.buts_shape = Button(self.frame_options_but, text="Mostrar mariposas de forma parecida", width=35, command=self.comp_shape)
            self.sh_hist = Button(self.frame_options_but, text="Mostrar histograma", width=35, command=self.show_hist)
            self.sh_msk = Button(self.frame_options_but, text="Mostrar mascara", width=35, command=self.show_msk)
            self.del_but = Button(self.frame_options_but, text="Eliminar mariposa", width=35, command=self.delete_but) 
                       
            lb_opc.grid(row=0, column=0)        
            self.buts_col.grid(row=1, column=0)
            self.buts_shape.grid(row=2, column=0)
            self.sh_hist.grid(row=3, column=0)
            self.sh_msk.grid(row=4, column=0)
            self.del_but.grid(row=5, column=0)
        
        MenuDemo._instance_but_act = self
            
        self.win_new_but.mainloop()   
        
    def delete_but(self):
        s = tkMessageBox.askquestion(None, "Esta seguro que quiere eliminar permanentemente este ejemplar?")
        if s == 'yes':
            if not(self.estudio):
                self.db.del_item(self.col_act,self.but_act)                
            self.but_act = Null
            self.update_frame_but(self.no_img)
            self._instance_but_act = None
            self.estudio = False
            self.win_new_but.destroy()
            self.set_col(self.col_act)
                            
    def comp_shape(self):
        '''TODO'''
        MenuDemo._instance_but_act = None
        self.win_new_but.destroy()
        
        c1 = self.but_act.get_cnt()
        s = tkMessageBox.askquestion(None, "Desea buscar similitudes con este ejemplar solo en la coleccion: "+self.col_act+'?')
        if s == 'yes':
            buts = self.db.get_buts_col(self.col_act)
        else:
            buts = self.db.get_buts() 
        vals = []
        some = False  
        #Las mariposas que se pasen de 1000 les ponemos valor negativo      
        for elem in buts:
            if self.but_act != elem and cv2.matchShapes(c1,elem.get_cnt(),1,0.0) < 0.06:
                vals.append(cv2.matchShapes(c1,elem.get_cnt(),1,0.0))
                some = True
            else:
                vals.append(-1)
        #Ordenamos los arrays de mayor parecido a menos
        count = len(vals) 
        vals_neg = 0
        for i in range(count):       
            if vals[i] == -1:
                vals_neg = vals_neg + 1
        vals, buts = bubbleSort(vals, buts)
                
        #Eliminamos las posiciones negativas del array
        for i in range(vals_neg):
            del vals[0]
            del buts[0]
        
        if (some):    
            self.show_similar_buts('Color',buts,vals)
        else:
            tkMessageBox.showwarning('Comparacion por color', 'No se encontro ninguna mariposa parecida!')
        
    def comp_color(self):
        MenuDemo._instance_but_act = None
        self.win_new_but.destroy()
        h1 = self.but_act.get_hist()
        s = tkMessageBox.askquestion(None, "Desea buscar similitudes con este ejemplar solo en la coleccion: "+self.col_act+'?')
        if s == 'yes':
            buts = self.db.get_buts_col(self.col_act)
        else:
            buts = self.db.get_buts()            
        vals = []
        some = False  
        #Las mariposas que se pasen de 1000 les ponemos valor negativo      
        for elem in buts:
            if self.but_act != elem and compare_hist(h1,elem.get_hist()) < 1000:
                vals.append(compare_hist(h1,elem.get_hist()))
                some = True
            else:
                vals.append(-1)
        #Ordenamos los arrays de mayor parecido a menos
        count = len(vals) 
        vals_neg = 0
        for i in range(count):       
            if vals[i] == -1:
                vals_neg = vals_neg + 1
        vals, buts = bubbleSort(vals, buts)
                
        #Eliminamos las posiciones negativas del array
        for i in range(vals_neg):
            del vals[0]
            del buts[0]
        
        if (some):    
            self.show_similar_buts('Color',buts,vals)
        else:
            tkMessageBox.showwarning('Comparacion por color', 'No se encontro ninguna mariposa parecida!')
        
    def show_similar_buts(self,tipo,buts,vals):       
        
        self.win_similar_buts= Toplevel()
        
        self.canvas=Canvas(self.win_similar_buts)
        fr_similar_buts = Frame(self.canvas)
        myscrollbar=Scrollbar(self.win_similar_buts,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        
        myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=fr_similar_buts,anchor='nw')
        fr_similar_buts.bind("<Configure>",self.myfunction)
        
        self.btn_sim_buts = {}
        index = 0
        for elem in buts:
            action = lambda x = elem: self.set_frame_central(x)
            self.btn_sim_buts[index] = Button(fr_similar_buts, image=elem.get_min_img(), command=action)
            self.btn_sim_buts[index].pack()
            index = index + 1
            
    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=345,height=560)        
        
    def show_msk(self):
        MenuDemo._instance_but_act = None
        self.win_new_but.destroy()
        cv2.imshow('Mascara', self.but_act.get_mask())
        
        
        
    #Insertamos una nueva mariposa en la base de datos    
    def insert_but(self):
        s = tkMessageBox.askquestion(None, "Desea introducir este ejemplar en la coleccion de "+self.col_act+'?')
        if s == 'yes':
            #Cerramos la ventana de opciones
            MenuDemo._instance_but_act = None
            self.win_new_but.destroy()    
            self.get_dist03_but() 
            self.db.new_but(self.but_act,self.col_act)
            self.estudio = False
            self.show_buts(self.db.get_buts_col(self.col_act))
            self.prev_but()
            
    def on_closing(self):
        try:
            self.db.save_db(self.col_act)
        except: 
            print 'Error al guardar la base de datos'
        self.master.destroy()   
            
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
           
def bubbleSort(lista,lista2):
    comparaciones = 0
    n = len(lista)
 
    for i in xrange(1, n):
        for j in xrange(n-i):
            comparaciones += 1
 
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
                lista2[j], lista2[j+1] = lista2[j+1], lista2[j]
    return lista,lista2
         
if __name__ == '__main__':
    MenuDemo().mainloop()