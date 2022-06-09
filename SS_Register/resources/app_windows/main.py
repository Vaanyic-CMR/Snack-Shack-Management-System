from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font

from . import (
    camper_transactions as camperT,
    tshirt_handout as ts_handout,
    staff_transactions as staffT,
    cash_transactions as cashT,
    settings as sett_window
)
from .. import (
    var_const as vc,
    client
)

class Main:
    def __init__(self) -> None:
        # --------------------- Title Bar and General
        self.master = Tk()
        self.master.title("Snack Shack Management System | Register")
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
        
        s = ttk.Style()
        s.theme_use('vista') # Default is "vista"
        s.configure('TNotebook.Tab', font=self.base_font)
        s.configure("TCombobox", borderwidth=5 )
        
        # ----- Constructing widgets
        self.__menu_bar()
        self.__build_title()
        self.__build_nav_buttons()
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
    
    def __build_title( self ):
        Label(self.master, text="Snack Shack Management System\nRegister", bg="light grey",
                font=self.title_font
            ).pack(padx=10)
        ttk.Separator(self.master, orient="horizontal").pack(fill=X, expand=True, pady=(5, 20))
    def __build_nav_buttons( self ):
        btnCamper = Button(self.master, text="Camper Transactions", font=self.base_font,
                        command=self.open_camper_transactions)
        btnCamper.pack( padx=10, pady=5 )
        btnStaff = Button(self.master, text="Staff Transactions", font=self.base_font,
                        command=self.open_staff_transactions)
        btnStaff.pack( padx=10, pady=5 )
        btnCT = Button(self.master, text="Cash Transaction", font=self.base_font,
                    command=self.open_cash_transactions)
        btnCT.pack( padx=10, pady=5 )
        btnHandout = Button(self.master, text="T-Shirt Handouts", font=self.base_font,
                    command=self.open_tshirt_handouts)
        btnHandout.pack( padx=10, pady=5 )
    
    # ------------------ Open Window Methods
    def open_camper_transactions( self ):
        try:
            if client.client is None:
                client.connect_to_host()
            self.master.destroy()
            camperT.CamperTransactions()
        except Exception as e:
            messagebox.showerror(
                "Network Error",
                f"There was a problem connecting to the server.\n{e}"
            )
    def open_staff_transactions( self ):
        try:
            if client.client is None:
                client.connect_to_host()
            self.master.destroy()
            staffT.StaffTransactions()
        except Exception as e:
            messagebox.showerror(
                "Network Error",
                f"There was a problem connecting to the server.\n{e}"
            )
    def open_cash_transactions( self ):
        try:
            if client.client is None:
                client.connect_to_host()
            self.master.destroy()
            cashT.CashTransactions()
        except Exception as e:
            messagebox.showerror(
                "Network Error",
                f"There was a problem connecting to the server.\n{e}"
            )
    def open_tshirt_handouts( self ):
        try:
            if client.client is None:
                client.connect_to_host()
            self.master.destroy()
            ts_handout.TShirtHandout()
        except Exception as e:
            messagebox.showerror(
                "Network Error",
                f"There was a problem connecting to the server.\n{e}"
            )