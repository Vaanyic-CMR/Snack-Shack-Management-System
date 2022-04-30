from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font

from ... import (
    var_const as vc,
    client
)

class TransactionRow:
    def __init__(self, frame, data, on_update) -> None:
        # Adding row data to instance.
        self.data = data
        self.on_update = on_update
        
        # --------------------- Fonts & Style
        self.title_font = Font(
            family = vc.settings.title_font["family"],
            size = vc.settings.title_font["size"],
            weight = vc.settings.title_font["weight"]
        )
        self.base_font = Font(
            family = vc.settings.base_font["family"],
            size = vc.settings.base_font["size"]
        )
        
        # ----- Set up row Frame
        self.row_frame = Frame( frame )
        self.row_frame.pack()
        
        # ----- Build Row
        self.__build_default_items()
        self.__build_clothing_sizes()
        
        Grid.columnconfigure(self.row_frame, 0, weight=1)
        Grid.columnconfigure(self.row_frame, 2, weight=1)
        Grid.columnconfigure(self.row_frame, 4, weight=1)
        Grid.columnconfigure(self.row_frame, 6, weight=1)
        Grid.columnconfigure(self.row_frame, 8, weight=1)
        Grid.rowconfigure(self.row_frame, 1, weight=2)
        Grid.rowconfigure(self.row_frame, 2, weight=1)
    
    def __build_default_items( self ):
        # ----- Set up spinboxes
        Spinbox( self.row_frame, command=self.on_update, state='readonly',
            textvariable=self.data.col1["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=0, padx=5, pady=5 )
        Spinbox( self.row_frame, command=self.on_update, state='readonly',
            textvariable=self.data.col2["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=2, padx=5, pady=5 )
        Spinbox( self.row_frame, command=self.on_update, state='readonly',
            textvariable=self.data.col3["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=4, padx=5, pady=5 )
        Spinbox( self.row_frame, command=self.on_update, state='readonly',
            textvariable=self.data.col4["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=6, padx=5, pady=5 )
        Spinbox( self.row_frame, command=self.on_update, state='readonly',
            textvariable=self.data.col5["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=8, padx=5, pady=5 )
        
        # ----- Set up listboxes
        self.listbox_1 = Listbox( self.row_frame, height=18, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_1.grid( row=1, column=0, sticky=NSEW, padx=5, pady=5 )
        self.listbox_2 = Listbox( self.row_frame, height=18, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_2.grid( row=1, column=2, sticky=NSEW, padx=5, pady=5 )
        self.listbox_3 = Listbox( self.row_frame, height=18, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_3.grid( row=1, column=4, sticky=NSEW, padx=5, pady=5 )
        self.listbox_4 = Listbox( self.row_frame, height=18, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_4.grid( row=1, column=6, sticky=NSEW, padx=5, pady=5 )
        self.listbox_5 = Listbox( self.row_frame, height=18, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_5.grid( row=1, column=8, sticky=NSEW, padx=5, pady=5 )
        
        # ----- Bind listbox select updates.
        self.listbox_1.bind("<<ListboxSelect>>", self.listbox_1_select)
        self.listbox_2.bind("<<ListboxSelect>>", self.listbox_2_select)
        self.listbox_3.bind("<<ListboxSelect>>", self.listbox_3_select)
        self.listbox_4.bind("<<ListboxSelect>>", self.listbox_4_select)
        self.listbox_5.bind("<<ListboxSelect>>", self.listbox_5_select)
        
        # ----- Set up scrollbars
        scrollbar_1 = Scrollbar( self.row_frame, orient=VERTICAL )
        scrollbar_1.grid( row=1, column=1, sticky=NS )
        scrollbar_2 = Scrollbar( self.row_frame, orient=VERTICAL )
        scrollbar_2.grid( row=1, column=3, sticky=NS )
        scrollbar_3 = Scrollbar( self.row_frame, orient=VERTICAL )
        scrollbar_3.grid( row=1, column=5, sticky=NS )
        scrollbar_4 = Scrollbar( self.row_frame, orient=VERTICAL )
        scrollbar_4.grid( row=1, column=7, sticky=NS )
        scrollbar_5 = Scrollbar( self.row_frame, orient=VERTICAL )
        scrollbar_5.grid( row=1, column=9, sticky=NS )
        
        # ----- Configure listboxes & scrollbars.
        self.listbox_1.config( yscrollcommand=scrollbar_1.set )
        scrollbar_1.config( command=self.listbox_1.yview )
        self.listbox_2.config( yscrollcommand=scrollbar_2.set )
        scrollbar_2.config( command=self.listbox_2.yview )
        self.listbox_3.config( yscrollcommand=scrollbar_3.set )
        scrollbar_3.config( command=self.listbox_3.yview )
        self.listbox_4.config( yscrollcommand=scrollbar_4.set )
        scrollbar_4.config( command=self.listbox_4.yview )
        self.listbox_5.config( yscrollcommand=scrollbar_5.set )
        scrollbar_5.config( command=self.listbox_5.yview )
    def __build_clothing_sizes( self ):
        # ----- Set up listboxes
        self.cloth_listbox_1 = Listbox( self.row_frame, height=8, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.cloth_listbox_1.grid( row=2, column=0, sticky=NSEW, padx=5, pady=5 )
        self.cloth_listbox_2 = Listbox( self.row_frame, height=8, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.cloth_listbox_2.grid( row=2, column=2, sticky=NSEW, padx=5, pady=5 )
        self.cloth_listbox_3 = Listbox( self.row_frame, height=8, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.cloth_listbox_3.grid( row=2, column=4, sticky=NSEW, padx=5, pady=5 )
        self.cloth_listbox_4 = Listbox( self.row_frame, height=8, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.cloth_listbox_4.grid( row=2, column=6, sticky=NSEW, padx=5, pady=5 )
        self.cloth_listbox_5 = Listbox( self.row_frame, height=8, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.cloth_listbox_5.grid( row=2, column=8, sticky=NSEW, padx=5, pady=5 )
        
        sizes = ["C-Small", "C-Medium", "C-Large", "Small", "Medium", "Large", "X-Large", "XX-Large"]
        for size in sizes:
            self.cloth_listbox_1.insert(END, size)
            self.cloth_listbox_2.insert(END, size)
            self.cloth_listbox_3.insert(END, size)
            self.cloth_listbox_4.insert(END, size)
            self.cloth_listbox_5.insert(END, size)
        
        self.cloth_listbox_1.bind("<<ListboxSelect>>", self.cloth_listbox_1_select)
        self.cloth_listbox_2.bind("<<ListboxSelect>>", self.cloth_listbox_2_select)
        self.cloth_listbox_3.bind("<<ListboxSelect>>", self.cloth_listbox_3_select)
        self.cloth_listbox_4.bind("<<ListboxSelect>>", self.cloth_listbox_4_select)
        self.cloth_listbox_5.bind("<<ListboxSelect>>", self.cloth_listbox_5_select)
        
        self.cloth_listbox_1.config( state="disabled" )
        self.cloth_listbox_2.config( state="disabled" )
        self.cloth_listbox_3.config( state="disabled" )
        self.cloth_listbox_4.config( state="disabled" )
        self.cloth_listbox_5.config( state="disabled" )
    
    def populate_listboxes( self, items=[] ):
        self.listbox_1.delete(0, END), self.listbox_2.delete(0, END)
        self.listbox_3.delete(0, END), self.listbox_4.delete(0, END)
        self.listbox_5.delete(0, END)
        
        self.cloth_listbox_1.delete(0, END), self.cloth_listbox_2.delete(0, END)
        self.cloth_listbox_3.delete(0, END), self.cloth_listbox_4.delete(0, END)
        self.cloth_listbox_5.delete(0, END)
        
        for item in items:
            self.listbox_1.insert(END, item)
            self.listbox_2.insert(END, item)
            self.listbox_3.insert(END, item)
            self.listbox_4.insert(END, item)
            self.listbox_5.insert(END, item)
    def reset_widgets( self ):
        self.data.col1["spinbox_val"].set(0)
        self.data.col2["spinbox_val"].set(0)
        self.data.col3["spinbox_val"].set(0)
        self.data.col4["spinbox_val"].set(0)
        self.data.col5["spinbox_val"].set(0)
        
        self.listbox_1.selection_clear(0, END)
        self.listbox_2.selection_clear(0, END)
        self.listbox_3.selection_clear(0, END)
        self.listbox_4.selection_clear(0, END)
        self.listbox_5.selection_clear(0, END)
        
        self.cloth_listbox_1.selection_clear(0, END)
        self.cloth_listbox_2.selection_clear(0, END)
        self.cloth_listbox_3.selection_clear(0, END)
        self.cloth_listbox_4.selection_clear(0, END)
        self.cloth_listbox_5.selection_clear(0, END)
    
    def listbox_1_select( self, e=None ):
        self.data.col1["listbox_val"].set( self.listbox_1.get(ANCHOR) )
        cmd = ("api/inventory/item", self.listbox_1.get(ANCHOR))
        client.send( cmd )
        self.data.col1["item"] = client.response_from_server()
        
        if self.data.col1["item"].catagory == "Clothing":
            self.cloth_listbox_1.config( state="normal")
            messagebox.showinfo("Notice:", "Please Select 1 Size")
        else:
            self.cloth_listbox_1.config( state="disabled")
        self.on_update()
    def listbox_2_select( self, e=None ):
        self.data.col2["listbox_val"].set( self.listbox_2.get(ANCHOR) )
        cmd = ("api/inventory/item", self.listbox_2.get(ANCHOR))
        client.send( cmd )
        self.data.col2["item"] = client.response_from_server()
        
        if self.data.col2["item"].catagory == "Clothing":
            self.cloth_listbox_2.config( state="normal")
            messagebox.showinfo("Notice:", "Please Select 1 Size")
        else:
            self.cloth_listbox_2.config( state="disabled")
        self.on_update()
    def listbox_3_select( self, e=None ):
        self.data.col3["listbox_val"].set( self.listbox_3.get(ANCHOR) )
        cmd = ("api/inventory/item", self.listbox_3.get(ANCHOR))
        client.send( cmd )
        self.data.col3["item"] = client.response_from_server()
        
        if self.data.col3["item"].catagory == "Clothing":
            self.cloth_listbox_3.config( state="normal")
            messagebox.showinfo("Notice:", "Please Select 1 Size")
        else:
            self.cloth_listbox_3.config( state="disabled")
        self.on_update()
    def listbox_4_select( self, e=None ):
        self.data.col4["listbox_val"].set( self.listbox_4.get(ANCHOR) )
        cmd = ("api/inventory/item", self.listbox_4.get(ANCHOR))
        client.send( cmd )
        self.data.col4["item"] = client.response_from_server()
        
        if self.data.col4["item"].catagory == "Clothing":
            self.cloth_listbox_4.config( state="normal")
            messagebox.showinfo("Notice:", "Please Select 1 Size")
        else:
            self.cloth_listbox_4.config( state="disabled")
        self.on_update()
    def listbox_5_select( self, e=None ):
        self.data.col5["listbox_val"].set( self.listbox_5.get(ANCHOR) )
        cmd = ("api/inventory/item", self.listbox_5.get(ANCHOR))
        client.send( cmd )
        self.data.col5["item"] = client.response_from_server()
        
        if self.data.col5["item"].catagory == "Clothing":
            self.cloth_listbox_5.config( state="normal")
            messagebox.showinfo("Notice:", "Please Select 1 Size")
        else:
            self.cloth_listbox_5.config( state="disabled")
        self.on_update()
    
    def cloth_listbox_1_select( self, e=None ):
        self.data.col1["size_box_val"].set( self.cloth_listbox_1.get(ANCHOR) )
        print(self.data.col1["size_box_val"].get())
    def cloth_listbox_2_select( self, e=None ):
        self.data.col2["size_box_val"].set( self.cloth_listbox_2.get(ANCHOR) )
    def cloth_listbox_3_select( self, e=None ):
        self.data.col3["size_box_val"].set( self.cloth_listbox_3.get(ANCHOR) )
    def cloth_listbox_4_select( self, e=None ):
        self.data.col4["size_box_val"].set( self.cloth_listbox_4.get(ANCHOR) )
    def cloth_listbox_5_select( self, e=None ):
        self.data.col5["size_box_val"].set( self.cloth_listbox_5.get(ANCHOR) )
    