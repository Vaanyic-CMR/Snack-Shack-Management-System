from tkinter import *
from tkinter.font import Font

from ... import var_const as vc

class InputPrompt:
    def __init__(self, title, return_data) -> None:
        self.master = Toplevel()
        self.master.title(f"SSMS | {title}")
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
        
        self.return_data = return_data
        self.entry_data = IntVar(value=float(return_data.get()[1:]))
        
        Label( self.master, text=f"Enter {title}:", font=self.title_font, bg="light grey" ).pack( side=LEFT, padx=10, pady=10 )
        Entry( self.master, textvariable=self.entry_data, font=self.base_font, borderwidth=5 ).pack( side=LEFT, padx=10, pady=10 )
        Button( self.master, text="Submit", command=self.handle_submit ).pack( side=LEFT, padx=10, pady=10 )
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
    
    def handle_submit( self ):
        self.return_data.set(
            "${:,.2f}".format(self.entry_data.get())
        )
        self.master.destroy()