from tkinter import *
from tkinter.font import Font

from ... import var_const as vc

class InputPrompt:
    def __init__(self, title, return_data, update) -> None:
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
        self.update = update
        self.entry_data = StringVar(value=float(return_data.get()[1:]))
        
        Label( self.master, text=f"Enter {title}:", font=self.title_font, bg="light grey" ).pack( side=LEFT, padx=10, pady=10 )
        entry = Entry( self.master, textvariable=self.entry_data, font=self.base_font, borderwidth=5 )
        entry.pack( side=LEFT, padx=10, pady=10 )
        entry.bind("<Return>", self.handle_submit)
        Button( self.master, text="Submit", font=self.base_font,
            borderwidth=5, padx=5, command=self.handle_submit
        ).pack( side=LEFT, padx=10, pady=10 )
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
    
    def handle_submit( self, e=None ):
        self.return_data.set(
            "${:,.2f}".format(float(self.entry_data.get()))
        )
        self.update()
        self.master.destroy()