from tkinter import *
from tkinter import ttk
from tkinter.font import Font

from .. import var_const as vc

from ..models import bank

class ChangeYear:
    def __init__( self, main ):
        self.main_window = main
        
        # --------------------- Title Bar and General
        self.master = Toplevel()
        self.master.title("SSMS | Change Active Year")
        self.master.iconbitmap("resources/images/logo.ico")
        self.master.grab_set()
        
        # --------------------- Screen and Window Dimensions
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.window_width = int( self.screen_width*0.30 )
        self.window_height = int( self.screen_height*0.30 )
        
        self.window_position_x = int( self.screen_width/2 - self.window_width/2 )
        self.window_position_y = int( self.screen_height/2 - self.window_height/2 )
        
        self.master.geometry( f"+{ self.window_position_x }+{ self.window_position_y }" )
        
        # --------------------- Font Variables
        self.title_font = Font(
            family = vc.settings.title_font["family"],
            size = vc.settings.title_font["size"],
            weight = vc.settings.title_font["weight"]
            )
        self.base_font = Font(
            family = vc.settings.base_font["family"],
            size = vc.settings.base_font["size"]
            )
        
        self.years = bank.Bank.get_all_years()
        self.year = StringVar( value=vc.active_year )
        
        Label( self.master, text="Selected Year:", font=self.base_font
            ).pack( side=LEFT, padx=10, pady=30 )
        self.year_menu = OptionMenu( self.master, self.year, *self.years, command=self.update_year )
        self.year_menu.config( font=self.base_font )
        self.master.nametowidget(self.year_menu.menuname).config( font=self.base_font )
        self.year_menu.pack( side=LEFT, padx=10, pady=30 )
        
    def update_year( self, e=None ):
        vc.change_active_year( self.year.get() )
        self.main_window.update_tables()