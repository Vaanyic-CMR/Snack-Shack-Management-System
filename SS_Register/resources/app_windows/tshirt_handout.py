from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font

from datetime import datetime

from . import (
    main as main_window,
    settings as sett_window
)
from .. import (
    var_const as vc,
    client
)

class TShirtHandout:
    purchase_time_format = "%a, %b %d, %Y | %I:%M:%S %p"
    
    def __init__( self ) -> None:
        # --------------------- Title Bar and General
        self.master = Tk()
        self.master.title("SSMS | T-Shirt Handouts")
        self.master.iconbitmap("resources/images/logo.ico")
        self.master.config( bg="light grey" )
        
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
        self.list_font = Font(
            family = vc.settings.list_font["family"],
            size = vc.settings.list_font["size"]
        )
        
        s = ttk.Style()
        s.theme_use('vista') # Default is "vista"
        
        # ----- Variables
        self.tshirt_name = StringVar( value="Select A T-Shirt")
        self.tshirt_list = list()
        self.__load_tshirt_names()
        self.name = StringVar()
        self.selected_size = StringVar()
        self.tshirt = None
        
        # ----- Constructing widgets
        self.__menu_bar()
        self.__build_widgets()
        self.__set_geometery()
    
    # --------------------- Screen and Window Dimensions
    def __set_geometery( self ):
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.window_width = int( self.screen_width*0.30 )
        self.window_height = int( self.screen_height*0.30 )
        
        self.window_position_x = int( self.screen_width/2 - self.window_width/2 )
        self.window_position_y = int( self.screen_height/2 - self.window_height/2 )
        
        self.master.geometry( f"+{ self.window_position_x }+{ self.window_position_y }" )
    def __menu_bar( self ):
        self.t_menu = Menu(self.master)
        self.master.config(menu=self.t_menu, padx=20, pady=20)

        # File Menu
        self.file_menu = Menu(self.t_menu, tearoff = False)
        self.t_menu.add_cascade(label='File', menu = self.file_menu)
        self.file_menu.add_command(label='Exit', command = self.master.destroy)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='New List(s)')#, command = self.openCreate)
        
        # Options Menu
        self.option_menu = Menu(self.t_menu, tearoff=False)
        self.t_menu.add_cascade(label='Options', menu=self.option_menu)
        # self.option_menu.add_separator()
        self.option_menu.add_command(label='Settings', command=lambda : sett_window.Settings(self, "main"))
        self.option_menu.add_command(label='About')#, command=self.openAbout)
    
    # ---------------------- Build Layout
    def __build_widgets( self ):
        tshirt_menu = OptionMenu( self.master, self.tshirt_name, *self.tshirt_list, command=self.__get_tshirt )
        tshirt_menu.config( font=self.list_font )
        self.master.nametowidget(tshirt_menu.menuname).config( font=self.list_font )
        tshirt_menu.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.name_entry = Entry( self.master, font=self.base_font, width=15,
            textvariable=self.name
        )
        self.name_entry.grid(row=1, column=0, columnspan=2, padx=10)
        self.name_entry.focus()
        
        self.cloth_listbox = Listbox( self.master, height=8, selectmode='single',
            exportselection=False, font=self.list_font
        )
        self.cloth_listbox.grid( row=2, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5 )
        self.cloth_listbox.bind("<<ListboxSelect>>", self.__cloth_listbox_select)
        self.__load_sizes()
        
        Button(self.master, text="Submit", font=self.base_font,
            command=self.submit
        ).grid(row=3, column=0, padx=10)
        Button(self.master, text="Return to Menu", font=self.base_font,
            command=self.return_to_menu
        ).grid(row=3, column=1, padx=10)
    def __reset_selection( self ):
        self.cloth_listbox.selection_clear(0, END)
        self.name.set("")
        self.name_entry.focus()
    
    # --------------------- Load Data
    def __load_tshirt_names( self ):
        cmd = ("api/inventory/cloth_names", None)
        client.send( cmd )
        self.tshirt_list = client.response_from_server()
    def __load_sizes( self ):
        sizes = ["C-Small", "C-Medium", "C-Large", "Small", "Medium", "Large", "X-Large", "XX-Large"]
        for size in sizes:
            self.cloth_listbox.insert(END, size)
    
    # --------------------- Process Interactions
    def __get_tshirt( self, e=None ):
        cmd = ("api/inventory/item", self.tshirt_name.get())
        client.send( cmd )
        self.tshirt = client.response_from_server()
        
        if self.tshirt.in_stock == 0:
            messagebox.showwarning("Inventory Warning", "This item is out of stock")
    def __cloth_listbox_select( self, e=None ):
        self.selected_size.set( self.cloth_listbox.get(ANCHOR) )
        for size in self.tshirt.sizes:
            if size.size == self.selected_size.get() and size.in_stock == 0:
                messagebox.showwarning("Inventory Warning", "This item is out of stock")
    
    # --------------------- Button Interactions
    def submit( self ):
        items = [(
            f"{self.tshirt_name.get()} | {self.selected_size.get()}",
            1
        )]
        
        now = datetime.now()
        purchase_info = {
            "date_time": now.strftime(self.__class__.purchase_time_format),
            "customer_name": "",
            "purchase_type": "T-Shirt Handout",
            "items": items,
            "sum_total": "$0.00"
        }
        if self.name.get() == "":
            messagebox.showerror("Invalid Input", "Please enter name into name field.")
            return None
        else:
            purchase_info["customer_name"] = self.name.get()
        
        # ---------- Sending to Server.
        cmd = ("api/history/new_purchase", purchase_info)
        client.send( cmd )
        res = client.response_from_server()
        
        if res == client.SUCCESS_MSG:
            self.__get_tshirt()
            self.__reset_selection()
        elif res == client.FAIL_MSG:
            messagebox.showerror("Error", "Failed to process request.")
            return None
    def return_to_menu( self ):
        self.master.destroy()
        main_window.Main()