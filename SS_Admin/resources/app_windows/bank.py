from tkinter import *
from tkinter.font import Font

from .. import var_const as vc
from ..models import bank

class Bank:
    def __init__( self, main ):
        self.main_window = main
        
        # --------------------- Title Bar and General
        self.master = Toplevel()
        self.master.title("SSMS | Bank")
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
        
        # --------------------- Menu Bar
        self.menu_bar = Menu( self.master )
        self.master.config( menu = self.menu_bar )

        # File Menu
        self.file_menu = Menu( self.menu_bar, tearoff=False )
        self.menu_bar.add_cascade( label='File', menu=self.file_menu )
        self.file_menu.add_command( label='Exit', command=self.master.destroy )

        # Options Menu
        self.option_menu = Menu( self.menu_bar, tearoff = False )
        self.menu_bar.add_cascade( label = 'Options', menu = self.option_menu )
        self.option_menu.add_command( label = 'About')#, command = self.openAbout )
        
        # --------------------- Variables
        self.years = bank.Bank.get_all_years()
        self.year = StringVar( value=self.years[-1] )
        self.bank_total = IntVar()
        
        self.cash_total = IntVar()
        self.check_total = IntVar()
        self.card_total = IntVar()
        self.scholar_total = IntVar()
        
        self.camper_total = IntVar()
        self.staff_total = IntVar()
        
        # --------------------- Initialize Base Layout.
        # ----- Frames
        self.west_frame = Frame( self.master, padx=10, pady=10 )
        self.west_frame.pack( side=LEFT, fill=BOTH, expand=True )
        self.frame_1 = Frame( self.west_frame )
        self.frame_1.pack( fill=BOTH, expand=True )
        self.frame_2 = Frame( self.west_frame )
        self.frame_2.pack( fill=BOTH, expand=True )
        self.east_frame = Frame( self.master, padx=10, pady=10 )
        self.east_frame.pack( side=LEFT, fill=BOTH, expand=True )
        
        # ----- Fill Frame Content
        self.__build_frame_1()
        self.__build_frame_2()
        self.__build_east_frame()
        self.__set_geometery()
        
        # ----- Fill in Data
        self.__update_content()
    
    # --------------------- Screen and Window Dimensions
    def __set_geometery( self ):
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.window_width = int( self.screen_width*0.30 )
        self.window_height = int( self.screen_height*0.30 )
        
        self.window_position_x = int( self.screen_width/2 - self.window_width/2 )
        self.window_position_y = int( self.screen_height/2 - self.window_height/2 )
        
        self.master.geometry( f"+{ self.window_position_x }+{ self.window_position_y }" )
    
    def __build_frame_1( self ):
        Label( self.frame_1, text="Notice: use only to fix errors.", font=self.title_font
            ).grid( row=0, column=0, columnspan=2, pady=10 )
        
        Label( self.frame_1, text="Bank Total", font=self.base_font
            ).grid( row=1, column=0 )
        self.bank_total_entry = Entry( self.frame_1, borderwidth=5, textvariable=self.bank_total, font=self.base_font )
        self.bank_total_entry.bind( "<Return>", self.save )
        self.bank_total_entry.bind( "<Shift-Return>", self.delete )
        self.bank_total_entry.grid( row=2, column=0 )
        
        Label( self.frame_1, text="Selected Year:", font=self.base_font
            ).grid( row=1, column=1 )
        self.year_menu = OptionMenu( self.frame_1, self.year, *self.years, command=self.__update_content )
        self.year_menu.config( font=self.base_font )
        self.master.nametowidget(self.year_menu.menuname).config( font=self.base_font )
        self.year_menu.grid( row=2, column=1 )
    def __build_frame_2( self ):
        Label( self.frame_2, text="Camper Total", font=self.base_font
            ).grid( row=0, column=0 )
        self.camper_total_entry = Entry( self.frame_2, borderwidth=5, textvariable=self.camper_total, font=self.base_font )
        self.camper_total_entry.bind( "<Return>", self.save )
        self.camper_total_entry.bind( "<Shift-Return>", self.delete )
        self.camper_total_entry.grid( row=1, column=0 )
        
        Label( self.frame_2, text="Staff Total", font=self.base_font
            ).grid( row=0, column=1 )
        self.staff_total_entry = Entry( self.frame_2, borderwidth=5, textvariable=self.staff_total, font=self.base_font )
        self.staff_total_entry.bind( "<Return>", self.save )
        self.staff_total_entry.bind( "<Shift-Return>", self.delete )
        self.staff_total_entry.grid( row=1, column=1 )
    def __build_east_frame( self ):
        Label( self.east_frame, text="Cash Total", font=self.base_font
            ).grid( row=0, column=0 )
        self.cash_total_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.cash_total, font=self.base_font )
        self.cash_total_entry.bind( "<Return>", self.save )
        self.cash_total_entry.bind( "<Shift-Return>", self.delete )
        self.cash_total_entry.grid( row=1, column=0 )
        
        Label( self.east_frame, text="Check Total", font=self.base_font
            ).grid( row=0, column=1 )
        self.check_total_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.check_total, font=self.base_font )
        self.check_total_entry.bind( "<Return>", self.save )
        self.check_total_entry.bind( "<Shift-Return>", self.delete )
        self.check_total_entry.grid( row=1, column=1 )
        
        Label( self.east_frame, text="Card Total", font=self.base_font
            ).grid( row=2, column=0 )
        self.card_total_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.card_total, font=self.base_font )
        self.card_total_entry.bind( "<Return>", self.save )
        self.card_total_entry.bind( "<Shift-Return>", self.delete )
        self.card_total_entry.grid( row=3, column=0 )
        
        Label( self.east_frame, text="Scholarhip Total", font=self.base_font
            ).grid( row=2, column=1 )
        self.scholar_total_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.scholar_total, font=self.base_font )
        self.scholar_total_entry.bind( "<Return>", self.save )
        self.scholar_total_entry.bind( "<Shift-Return>", self.delete )
        self.scholar_total_entry.grid( row=3, column=1 )
        
        Button( self.east_frame, text="Save\n(Return)", font=self.base_font, command=self.save, padx=20
            ).grid( row=4, column=0, padx=10, pady=30 )
        Button( self.east_frame, text="Delete\n(Shift+Return)", font=self.base_font, command=self.delete, padx=20
            ).grid( row=4, column=1, padx=10, pady=30 )
    
    def __reset_content( self, e=None ):
        self.year.set( self.years[-1] )
        self.__update_content()
    def __update_content( self, e=None ):
        data = bank.Bank.get_by_year( self.year.get() )
        self.bank_total.set( data.bank_total )
        
        self.cash_total.set( data.cash_total )
        self.check_total.set( data.check_total )
        self.card_total.set( data.card_total )
        self.scholar_total.set( data.scholar_total )
        
        self.camper_total.set( data.camper_total )
        self.staff_total.set( data.staff_total )
    
    def save( self, e=None ):
        bank.Bank.save({
            "year": self.year.get(),
            "bank_total": self.bank_total.get(),
            
            "cash_total": self.cash_total.get(),
            "check_total": self.check_total.get(),
            "card_total": self.card_total.get(),
            "scholar_total": self.scholar_total.get(),
            
            "camper_total": self.camper_total.get(),
            "staff_total": self.staff_total.get()
        })
        self.__reset_content()
    def delete( self, e=None ):
        bank.Bank.delete( year=self.year.get() )
        self.__reset_content()
    