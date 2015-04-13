'''
Created on 26/3/2015

@author: Psilocibino
'''
# File: panels.py
# References:
#    http://hg.python.org/cpython/file/4e32c450f438/Lib/tkinter/simpledialog.py
#    http://docs.python.org/py3k/library/inspect.html#module-inspect
#
# Icons sourced from:
#    http://findicons.com/icon/69404/deletered?width=16#
#    http://findicons.com/icon/93110/old_edit_find?width=16#
 
from Tkinter import *
import ttk 
import Dialog
import Image, ImageTk
import inspect
from Tkconstants import TOP, BOTTOM, LEFT, HORIZONTAL, ACTIVE, EW, BOTH, WORD, VERTICAL, NSEW, E, W, RIGHT
from telnetlib import theNULL
 
'''class MsgPanel(ttk.Frame):
    def __init__(self, master, msgtxt):
        ttk.Frame.__init__(self, master)
        self.pack(side=TOP, fill=X)
         
        msg = self.Label(self, wraplength='4i', justify=LEFT)
        msg['text'] = ''.join(msgtxt)
        msg.pack(fill=X, padx=5, pady=5)'''
         
class SeePanel(ttk.Frame):
    def __init__(self, master,img):
        ttk.Frame.__init__(self, master)
        self.pack(side=BOTTOM, fill=X)          # resize with parent
         
        # separator widget
        sep = ttk.Separator(orient=HORIZONTAL)
 
        # Dismiss button
        print type(img)
        
        im = Image.open('img.jpg')   # image file
        imh = ImageTk.PhotoImage(im)
        print type(im)
        # handle to file
        dismissBtn = ttk.Button(text='Dismiss', image=imh, command=self.winfo_toplevel().destroy)
        dismissBtn.image = imh                  # prevent image from being garbage collected
        dismissBtn['compound'] = LEFT           # display image to left of label text
         
        # 'See Code' button
        im = Image.open('upload.jpg')
        imh = ImageTk.PhotoImage(im)
        codeBtn = ttk.Button(text='New butterfly...', image=imh, default=ACTIVE, command=lambda: CodeDialog(self.master))
        codeBtn.image = imh
        codeBtn['compound'] = LEFT
        codeBtn.focus()
                 
        # position and register widgets as children of this frame
        sep.grid(in_=self, row=0, columnspan=4, sticky=EW, pady=5)
        codeBtn.grid(in_=self, row=1, column=0, sticky=E)
        dismissBtn.grid(in_=self, row=1, column=1, sticky=E)
         
        # set resize constraints
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
 
        # bind <Return> to demo window, activates 'See Code' button;
        # <'Escape'> activates 'Dismiss' button
        self.winfo_toplevel().bind('<Return>', lambda x: codeBtn.invoke() )
        self.winfo_toplevel().bind('<Escape>', lambda x: dismissBtn.invoke() )
 
class CodeDialog():
    
    #Create a modal dialog to display a demo's source code file.
         
    def body(self, master):
        """Overrides Dialog.body() to populate the dialog window with a scrolled text window
        and custom dialog buttons. """
         
        # get the full path of this object's parent source code file
        fileName = inspect.getsourcefile(self.parent._create_widgets)
         
        self.title('Source Code: ' + fileName)
         
        # create scrolled text widget
        txtFrame = ttk.Frame(self)
        txtFrame.pack(side=TOP, fill=BOTH)
         
        text = self.Text(txtFrame, height=24, width=100, wrap=WORD, setgrid=1, highlightthickness=0, pady=2, padx=3)
        xscroll = ttk.Scrollbar(txtFrame, command=text.xview, orient=HORIZONTAL)
        yscroll = ttk.Scrollbar(txtFrame, command=text.yview, orient=VERTICAL)
        text.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
         
        # position in frame and set resize constraints
        text.grid(row=0, column=0, sticky=NSEW)
        yscroll.grid(row=0, column=1, sticky=NSEW)
        txtFrame.rowconfigure(0, weight=1)
        txtFrame.columnconfigure(0, weight=1)
         
        # add text of file to scrolled text widget
        text.delete('0.0')
        text.insert(open(fileName).read())
 
    def buttonbox(self):
        """Overrides Dialog.buttonbox() to create custom buttons for this dialog. """
         
        box = ttk.Frame(self)
 
        # Cancel button
        cancelBtn = ttk.Button(box, text='Cancel', command=self.cancel)       
        cancelBtn.pack(side=RIGHT, padx=5, pady=5)
        self.bind('<Return>', self.cancel)
        self.bind('<Escape>', self.cancel)
         
        box.pack()