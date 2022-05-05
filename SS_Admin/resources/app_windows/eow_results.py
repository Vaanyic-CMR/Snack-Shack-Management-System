from tkinter import *
from tkinter import ttk
from tkinter.font import Font

from .. import var_const as vc

class EOWResults:
    def __init__( self, results ):
        # --------------------- Title Bar and General
        self.master = Toplevel()
        self.master.title("SSMS | EOW Results")
        self.master.iconbitmap("resources/images/logo.ico")
        self.master.grab_set()
        
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
        
        # -------------- Setting Canvas
        self.body_canvas = Canvas( self.master )
        self.body_canvas.pack( side=LEFT, fill=BOTH, expand=True )
        body_scrollbar = ttk.Scrollbar( self.master , orient=VERTICAL, command=self.body_canvas.yview )
        body_scrollbar.pack( side=RIGHT, fill=Y )
        
        # Configure Canvas
        self.body_canvas.configure( yscrollcommand=body_scrollbar.set )
        self.body_canvas.bind( '<Configure>',
            lambda e: self.body_canvas.configure(scrollregion=self.body_canvas.bbox("all")) )
        self.body_canvas.bind_all("<MouseWheel>", self.__on_mousewheel)
        
        # New canvas frame
        canvas_frame = Frame( self.body_canvas )
        self.body_canvas.create_window((0,0), window=canvas_frame, anchor=NW )
        
        for result in results:
            Label(canvas_frame, text=result.to_string(), font=self.base_font, borderwidth=8
                ).pack(pady=10, anchor="w", fill=BOTH, expand=True)
            ttk.Separator(canvas_frame, orient="horizontal"
                ).pack(padx=5, fill=X, expand=True)
        
        self.__set_geometery()
    
    # --------------------- Screen and Window Dimensions
    def __set_geometery( self ):
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.window_width = int( self.screen_width*0.26 )
        self.window_height = int( self.screen_height*0.75 )
        
        self.window_position_x = int( self.screen_width/2 - self.window_width/2 )
        self.window_position_y = int( self.screen_height/2 - self.window_height/2 )
        
        self.master.geometry( f"""{self.window_width}x{self.window_height}+{ self.window_position_x }+{ self.window_position_y }""" )

    def __on_mousewheel(self, event):
        self.body_canvas.yview_scroll(int(-1*(event.delta/120)), "units")