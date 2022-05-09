from tkinter import *
from tkinter import ttk
from tkinter.font import Font

from .. import var_const as vc
from . import main
from ..models import settings as s_model

class Settings:
    def __init__( self, main=None ):
        self.main_window = main

        # --------------------- Title Bar and General
        self.master = Toplevel()
        self.master.title("SSMS | Settings")
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
        
        # -------------------- Tkinter Variables
        self.host_name = StringVar(value=vc.settings.host_name)
        self.port = IntVar(value=vc.settings.port)
        self.food_limit = StringVar(value=vc.settings.food_limit)
        
        self.dark_mode = BooleanVar(value=vc.settings.dark_mode)
        
        self.title_size = IntVar(value=vc.settings.title_font["size"])
        self.base_size = IntVar(value=vc.settings.base_font["size"])
        self.table_header_size = IntVar(value=vc.settings.table_header_font["size"])
        self.table_row_size = IntVar(value=vc.settings.table_row_font["size"])
        
        # -------------------- Build Main Structure
        Label( self.master, text="Settings:", font=self.title_font ).pack()
        ttk.Separator( self.master, orient="horizontal" ).pack(fill=BOTH, expand=True, pady=(5, 20))
        self.frame_1 = Frame( self.master )
        self.frame_1.pack(padx=10, pady=10)
        ttk.Separator( self.master, orient="horizontal" ).pack(fill=X, expand=True, pady=(5, 20))
        self.frame_2 = Frame( self.master )
        self.frame_2.pack(padx=10, pady=10)
        ttk.Separator( self.master, orient="horizontal" ).pack(fill=X, expand=True, pady=(5, 20))
        self.frame_3 = Frame( self.master )
        self.frame_3.pack(padx=10, pady=10)
        
        # -------------------- Save Button
        Button( self.master, text="Save & Restart", font=self.base_font,
                command=self.__save
            ).pack(pady=30)
        
        # -------------------- Build Frames
        self.__build_frame_1()
        self.__build_frame_2()
        self.__build_frame_3()
        
        self.__set_geometery()
    
    def __build_frame_1( self ):
        Label(self.frame_1, text="Server Hostname", anchor=W, font=self.base_font
            ).grid(row=0, column=0)
        Entry(self.frame_1, textvariable=self.host_name, borderwidth=5,
                state="readonly", font=self.base_font
            ).grid(row=1, column=0)
        
        Label(self.frame_1, text="Server Port", anchor=W, font=self.base_font
            ).grid(row=0, column=1)
        Entry(self.frame_1, textvariable=self.port, borderwidth=5,
                font=self.base_font
            ).grid(row=1, column=1)
    def __build_frame_2( self ):
        Label(self.frame_2, text="Title Font Size", font=self.base_font, anchor=W
            ).grid(row=0, column=0)
        Entry(self.frame_2, textvariable=self.title_size, borderwidth=5,
                font=self.base_font
            ).grid(row=1, column=0)
        
        Label(self.frame_2, text="Base Font Size", font=self.base_font, anchor=W
            ).grid(row=0, column=1)
        Entry(self.frame_2, textvariable=self.base_size, borderwidth=5,
                font=self.base_font
            ).grid(row=1, column=1)
        
        Label(self.frame_2, text="Table Header Font Size", font=self.base_font, anchor=W
            ).grid(row=2, column=0)
        Entry(self.frame_2, textvariable=self.table_header_size, borderwidth=5,
                font=self.base_font
            ).grid(row=3, column=0)
        
        Label(self.frame_2, text="Table Row Font Size", font=self.base_font, anchor=W
            ).grid(row=2, column=1)
        Entry(self.frame_2, textvariable=self.table_row_size, borderwidth=5,
                font=self.base_font
            ).grid(row=3, column=1)
    def __build_frame_3( self ):
        Label(self.frame_3, text="Food Limit", font=self.base_font, anchor=W
            ).grid(row=0, column=0)
        Entry(self.frame_3, textvariable=self.food_limit, borderwidth=5,
                font=self.base_font, state="disabled"
            ).grid(row=1, column=0)
        
        Checkbutton(self.frame_3, variable=self.dark_mode, text="Dark Mode",
                font=self.base_font, onvalue=True, offvalue=False
            ).grid(row=1, column=1)
    
    # --------------------- Screen and Window Dimensions
    def __set_geometery( self ):
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.window_width = self.master.winfo_width()#int( self.screen_width*0.30 )
        self.window_height = self.master.winfo_height()#int( self.screen_height*0.30 )
        
        self.window_position_x = int( self.screen_width/2 - self.window_width )
        self.window_position_y = int( self.screen_height/2 - self.window_height )
        
        self.master.geometry( f"+{ self.window_position_x }+{ self.window_position_y }" )
    
    def __save( self ):
        s_model.Settings.save({
            "host_name": self.host_name.get(),
            "port": self.port.get(),
            "food_limit": float(self.food_limit.get()),
            "dark_mode": self.dark_mode.get(),
            "title_font": {
                "family": "monospace",
                "size": self.title_size.get(),
                "weight": "bold"
            },
            "base_font": {
                "family": "monospace",
                "size": self.base_size.get()
            },
            "table_header_font": {
                "family": "monospace",
                "size": self.table_header_size.get(),
                "weight": "bold"
            },
            "table_row_font": {
                "family": "monospace",
                "size": self.table_row_size.get()
            }
        })
        vc.reload_settings()
        
        self.main_window.master.destroy()
        main.MainDisplay()