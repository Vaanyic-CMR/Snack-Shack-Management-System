from tkinter import *
from tkinter import ttk
from tkinter.font import Font

from ... import var_const as vc

class TransactionRow:
    def __init__(self, frame, data, on_update) -> None:
        # Adding row data to instance.
        self.data = data
        
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
        row_frame = Frame( frame )
        row_frame.pack()
        
        # ----- Set up spinboxes
        Spinbox( row_frame, command=on_update, state='readonly',
            textvariable=data.col1["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=0, padx=5, pady=5 )
        Spinbox( row_frame, command=on_update, state='readonly',
            textvariable=data.col2["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=2, padx=5, pady=5 )
        Spinbox( row_frame, command=on_update, state='readonly',
            textvariable=data.col3["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=4, padx=5, pady=5 )
        Spinbox( row_frame, command=on_update, state='readonly',
            textvariable=data.col4["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=6, padx=5, pady=5 )
        Spinbox( row_frame, command=on_update, state='readonly',
            textvariable=data.col5["spinbox_val"], from_=0, to=50,
            width=10, font=self.base_font
        ).grid( row=0, column=8, padx=5, pady=5 )
        
        # ----- Set up listboxes
        self.listbox_1 = Listbox( row_frame, height=25, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_1.grid( row=1, column=0, sticky=NSEW, padx=5, pady=5 )
        self.listbox_2 = Listbox( row_frame, height=25, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_2.grid( row=1, column=2, sticky=NSEW, padx=5, pady=5 )
        self.listbox_3 = Listbox( row_frame, height=25, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_3.grid( row=1, column=4, sticky=NSEW, padx=5, pady=5 )
        self.listbox_4 = Listbox( row_frame, height=25, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_4.grid( row=1, column=6, sticky=NSEW, padx=5, pady=5 )
        self.listbox_5 = Listbox( row_frame, height=25, selectmode='single',
            exportselection=False, font=self.base_font
        )
        self.listbox_5.grid( row=1, column=8, sticky=NSEW, padx=5, pady=5 )
        
        # ----- Set up scrollbars
        scrollbar_1 = Scrollbar( row_frame, orient=VERTICAL )
        scrollbar_1.grid( row=1, column=1, sticky=NS )
        scrollbar_2 = Scrollbar( row_frame, orient=VERTICAL )
        scrollbar_2.grid( row=1, column=3, sticky=NS )
        scrollbar_3 = Scrollbar( row_frame, orient=VERTICAL )
        scrollbar_3.grid( row=1, column=5, sticky=NS )
        scrollbar_4 = Scrollbar( row_frame, orient=VERTICAL )
        scrollbar_4.grid( row=1, column=7, sticky=NS )
        scrollbar_5 = Scrollbar( row_frame, orient=VERTICAL )
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
        
        Grid.columnconfigure(row_frame, 0, weight=1)
        Grid.columnconfigure(row_frame, 2, weight=1)
        Grid.columnconfigure(row_frame, 4, weight=1)
        Grid.columnconfigure(row_frame, 6, weight=1)
        Grid.columnconfigure(row_frame, 8, weight=1)
        Grid.rowconfigure(row_frame, 1, weight=1)
    
    def populate_listboxes( self, items=[] ):
        self.listbox_1.delete(0, END), self.listbox_2.delete(0, END)
        self.listbox_3.delete(0, END), self.listbox_4.delete(0, END)
        self.listbox_5.delete(0, END)
        
        for item in items:
            self.listbox_1.insert(END, item)
            self.listbox_2.insert(END, item)
            self.listbox_3.insert(END, item)
            self.listbox_4.insert(END, item)
            self.listbox_5.insert(END, item)
    