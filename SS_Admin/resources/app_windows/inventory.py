from tkinter import *
from tkinter import ttk
from tkinter.font import Font

from .. import var_const as vc
from .sub_components import msgbox
from ..models import (
    inventory as inv_m,
    shopping_list as shop_m
)

class Inventory:
    def __init__( self, main ):
        self.main_window = main
        
        # --------------------- Title Bar and General
        self.master = Toplevel()
        self.master.title("SSMS | Inventory")
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
        
        self.master.option_add('*TCombobox*Listbox.font', self.base_font)
        
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
        self.cmbo_item = StringVar()
        self.txt_price = DoubleVar()
        self.txt_staff_price = DoubleVar()
        self.txt_staff_price.trace_add( 'write', self.__on_price_change )
        self.staff_price_state = StringVar( value="disabled" )
        self.txt_total_stock = IntVar()
        self.txt_threshold = IntVar()
        
        self.catagory_list = ['Food & Drink', 'Clothing', 'Accessories', 'Miscellaneous']
        self.catagory = StringVar()
        self.catagory.set( self.catagory_list[0] )
        
        # ----- Sizes
        self.txt_Csmall = IntVar()
        self.txt_Csmall.trace_add( 'write', self.__on_change )
        self.txt_Cmedium = IntVar()
        self.txt_Cmedium.trace_add( 'write', self.__on_change )
        self.txt_Clarge = IntVar()
        self.txt_Clarge.trace_add( 'write', self.__on_change )
        self.txt_small = IntVar()
        self.txt_small.trace_add( 'write', self.__on_change )
        self.txt_medium = IntVar()
        self.txt_medium.trace_add( 'write', self.__on_change )
        self.txt_large = IntVar()
        self.txt_large.trace_add( 'write', self.__on_change )
        self.txt_Xlarge = IntVar()
        self.txt_Xlarge.trace_add( 'write', self.__on_change )
        self.txt_XXlarge = IntVar()
        self.txt_XXlarge.trace_add( 'write', self.__on_change )
        
        self.thres_Csmall = IntVar()
        self.thres_Cmedium = IntVar()
        self.thres_Clarge = IntVar()
        self.thres_small = IntVar()
        self.thres_medium = IntVar()
        self.thres_large = IntVar()
        self.thres_Xlarge = IntVar()
        self.thres_XXlarge = IntVar()

        # --------------------- Initialize Base Layout.
        # ----- Frames
        self.west_frame = Frame( self.master, padx=10, pady=20 )
        self.west_frame.pack( side=LEFT, fill=BOTH, expand=True )
        self.east_frame = Frame( self.master, padx=10, pady=10 )
        self.east_frame.pack( side=RIGHT, fill=BOTH, expand=True )
        
        # ----- Fill Frame Content
        self.__build_west_frame()
        self.__build_east_frame()
        self.__set_geometery()
        
        # ----- Fill in Data
        self.__update_cmbo()
    
    # --------------------- Screen and Window Dimensions
    def __set_geometery( self ):
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.window_width = self.master.winfo_width()# int( self.screen_width*0.30 )
        self.window_height = self.master.winfo_height()# int( self.screen_height*0.30 )
        
        self.window_position_x = int( self.screen_width/4 - self.window_width/2 )
        self.window_position_y = int( self.screen_height/4 - self.window_height/2 )
        
        self.master.geometry( f"""+{ self.window_position_x }+{ self.window_position_y }""" )
    
    # ----- West Frame
    def __build_west_frame( self ):
        Label( self.west_frame, text="Item Name", font=self.base_font
            ).grid( row=0, column=0, padx=10 )
        self.cmbo = ttk.Combobox( self.west_frame, textvariable=self.cmbo_item, font=self.base_font )
        self.cmbo.bind( "<<ComboboxSelected>>", self.__update_values )
        self.cmbo.bind( "<Return>", self.save_item )
        self.cmbo.bind( "<Shift-Return>", self.delete_item )
        self.cmbo.grid( row=1, column=0, padx=10, pady=5 )
        
        Label( self.west_frame, text="Item Price", font=self.base_font
            ).grid( row=0, column=1, padx=10 )
        self.entry_price = Entry( self.west_frame, borderwidth=5, textvariable=self.txt_price, font=self.base_font )
        self.entry_price.bind( "<Return>", self.save_item )
        self.entry_price.bind( "<Shift-Return>", self.delete_item )
        self.entry_price.grid( row=1, column=1, padx=10, pady=5 )
        
        Label( self.west_frame, text="# in Stock (Sets Total)", font=self.base_font
            ).grid( row=2, column=0, padx=10 )
        self.entry_total_stock = Entry( self.west_frame, borderwidth=5, textvariable=self.txt_total_stock, font=self.base_font )
        self.entry_total_stock.bind( "<Return>", self.save_item )
        self.entry_total_stock.bind( "<Shift-Return>", self.delete_item )
        self.entry_total_stock.grid( row=3, column=0, padx=10, pady=5 )
        
        Checkbutton( self.west_frame, text="Staff Price", font=self.base_font,
            variable=self.staff_price_state, onvalue="normal", offvalue="disabled",
            command=self.__handle_staff_price
        ).grid( row=2, column=1 )
        self.entry_staff_price = Entry( self.west_frame, borderwidth=5, textvariable=self.txt_staff_price,
            font=self.base_font, state="disabled"
        )
        self.entry_staff_price.bind( "<Return>", self.save_item )
        self.entry_staff_price.bind( "<Shift-Return>", self.delete_item )
        self.entry_staff_price.grid( row=3, column=1, padx=10, pady=5 )
        
        Label( self.west_frame, text="Shopping Threshold", font=self.base_font
            ).grid( row=4, column=0, padx=10 )
        self.entry_threshold = Entry( self.west_frame, borderwidth=5, textvariable=self.txt_threshold, font=self.base_font )
        self.entry_threshold.bind( "<Return>", self.save_item )
        self.entry_threshold.bind( "<Shift-Return>", self.delete_item )
        self.entry_threshold.grid( row=5, column=0, padx=10, pady=5 )
        
        Label( self.west_frame, text="Item Catagory", font=self.base_font
            ).grid( row=4, column=1, padx=10 )
        self.option_catagory = OptionMenu( self.west_frame, self.catagory, *self.catagory_list, command=self.__check_catagory )
        self.option_catagory.config( font=self.base_font )
        self.cat_menu = self.master.nametowidget(self.option_catagory.menuname)
        self.cat_menu.config( font=self.base_font )
        self.option_catagory.grid( row=5, column=1, padx=10, pady=5 )
        
        Button( self.west_frame, text="Save Item\n(Return)", font=self.base_font, command=self.save_item, padx=20
            ).grid( row=6, column=0, padx=10, pady=30 )
        Button( self.west_frame, text="Delete Item\n(Shift+Return)", font=self.base_font, command=self.delete_item, padx=20
            ).grid( row=6, column=1, padx=10, pady=30 )
    def __build_east_frame( self ):
        Label( self.east_frame, text="# in Stock", font=self.base_font
            ).grid( row=0, column=1, padx=10 )
        Label( self.east_frame, text="Threshold", font=self.base_font
            ).grid( row=0, column=2, padx=10 )
        
        Label( self.east_frame, text="C-Small", font=self.base_font
            ).grid( row=1, column=0, padx=10 )
        self.entry_Csmall = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_Csmall, font=self.base_font )
        self.entry_Csmall.bind( "<Return>", self.save_item )
        self.entry_Csmall.bind( "<Shift-Return>", self.delete_item )
        self.entry_Csmall.grid( row=1, column=1, padx=10, pady=5 )
        self.entry_thres_Csmall = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_Csmall, font=self.base_font )
        self.entry_thres_Csmall.bind( "<Return>", self.save_item )
        self.entry_thres_Csmall.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_Csmall.grid( row=1, column=2, padx=10, pady=5 )
        
        Label( self.east_frame, text="C-Medium", font=self.base_font
            ).grid( row=2, column=0, padx=10 )
        self.entry_Cmedium = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_Cmedium, font=self.base_font )
        self.entry_Cmedium.bind( "<Return>", self.save_item )
        self.entry_Cmedium.bind( "<Shift-Return>", self.delete_item )
        self.entry_Cmedium.grid( row=2, column=1, padx=10, pady=5 )
        self.entry_thres_Cmedium = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_Cmedium, font=self.base_font )
        self.entry_thres_Cmedium.bind( "<Return>", self.save_item )
        self.entry_thres_Cmedium.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_Cmedium.grid( row=2, column=2, padx=10, pady=5 )
        
        Label( self.east_frame, text="C-Large", font=self.base_font
            ).grid( row=3, column=0, padx=10 )
        self.entry_Clarge = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_Clarge, font=self.base_font )
        self.entry_Clarge.bind( "<Return>", self.save_item )
        self.entry_Clarge.bind( "<Shift-Return>", self.delete_item )
        self.entry_Clarge.grid( row=3, column=1, padx=10, pady=5 )
        self.entry_thres_Clarge = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_Clarge, font=self.base_font )
        self.entry_thres_Clarge.bind( "<Return>", self.save_item )
        self.entry_thres_Clarge.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_Clarge.grid( row=3, column=2, padx=10, pady=5 )
        
        Label( self.east_frame, text="Small", font=self.base_font
            ).grid( row=4, column=0, padx=10 )
        self.entry_small = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_small, font=self.base_font )
        self.entry_small.bind( "<Return>", self.save_item )
        self.entry_small.bind( "<Shift-Return>", self.delete_item )
        self.entry_small.grid( row=4, column=1, padx=10, pady=5 )
        self.entry_thres_small = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_small, font=self.base_font )
        self.entry_thres_small.bind( "<Return>", self.save_item )
        self.entry_thres_small.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_small.grid( row=4, column=2, padx=10, pady=5 )
        
        Label( self.east_frame, text="Medium", font=self.base_font
            ).grid( row=5, column=0, padx=10 )
        self.entry_medium = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_medium, font=self.base_font )
        self.entry_medium.bind( "<Return>", self.save_item )
        self.entry_medium.bind( "<Shift-Return>", self.delete_item )
        self.entry_medium.grid( row=5, column=1, padx=10, pady=5 )
        self.entry_thres_medium = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_medium, font=self.base_font)
        self.entry_thres_medium.bind( "<Return>", self.save_item )
        self.entry_thres_medium.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_medium.grid( row=5, column=2, padx=10, pady=5 )
        
        Label( self.east_frame, text="Large", font=self.base_font
            ).grid( row=6, column=0, padx=10 )
        self.entry_large = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_large, font=self.base_font )
        self.entry_large.bind( "<Return>", self.save_item )
        self.entry_large.bind( "<Shift-Return>", self.delete_item )
        self.entry_large.grid( row=6, column=1, padx=10, pady=5 )
        self.entry_thres_large = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_large, font=self.base_font )
        self.entry_thres_large.bind( "<Return>", self.save_item )
        self.entry_thres_large.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_large.grid( row=6, column=2, padx=10, pady=5 )
        
        Label( self.east_frame, text="X-Large", font=self.base_font
            ).grid( row=7, column=0, padx=10 )
        self.entry_Xlarge = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_Xlarge, font=self.base_font )
        self.entry_Xlarge.bind( "<Return>", self.save_item )
        self.entry_Xlarge.bind( "<Shift-Return>", self.delete_item )
        self.entry_Xlarge.grid( row=7, column=1, padx=10, pady=5 )
        self.entry_thres_Xlarge = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_Xlarge, font=self.base_font )
        self.entry_thres_Xlarge.bind( "<Return>", self.save_item )
        self.entry_thres_Xlarge.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_Xlarge.grid( row=7, column=2, padx=10, pady=5 )
        
        Label( self.east_frame, text="XX-Large", font=self.base_font
            ).grid( row=8, column=0, padx=10 )
        self.entry_XXlarge = Entry( self.east_frame, borderwidth=5, textvariable=self.txt_XXlarge, font=self.base_font )
        self.entry_XXlarge.bind( "<Return>", self.save_item )
        self.entry_XXlarge.bind( "<Shift-Return>", self.delete_item )
        self.entry_XXlarge.grid( row=8, column=1, padx=10, pady=5 )
        self.entry_thres_XXlarge = Entry( self.east_frame, borderwidth=5, textvariable=self.thres_XXlarge, font=self.base_font )
        self.entry_thres_XXlarge.bind( "<Return>", self.save_item )
        self.entry_thres_XXlarge.bind( "<Shift-Return>", self.delete_item )
        self.entry_thres_XXlarge.grid( row=8, column=2, padx=10, pady=5 )
        
        self.__check_catagory()
    
    def __update_cmbo( self ):
        self.ids_names = inv_m.Inventory.get_all_names()
        self.cmbo.config( value=self.ids_names )
    def __check_catagory( self, e=None ):
        if self.catagory.get() == "Clothing":
            self.txt_threshold.set( 0 )
            self.entry_total_stock.config( state="disabled" )
            self.entry_threshold.config( state="disabled" )
            self.entry_Csmall.config( state="normal" )
            self.entry_Cmedium.config( state="normal" )
            self.entry_Clarge.config( state="normal" )
            self.entry_small.config( state="normal" )
            self.entry_medium.config( state="normal" )
            self.entry_large.config( state="normal" )
            self.entry_Xlarge.config( state="normal" )
            self.entry_XXlarge.config( state="normal" )
            self.entry_thres_Csmall.config( state="normal" )
            self.entry_thres_Cmedium.config( state="normal" )
            self.entry_thres_Clarge.config( state="normal" )
            self.entry_thres_small.config( state="normal" )
            self.entry_thres_medium.config( state="normal" )
            self.entry_thres_large.config( state="normal" )
            self.entry_thres_Xlarge.config( state="normal" )
            self.entry_thres_XXlarge.config( state="normal" )
        else:
            self.entry_total_stock.config( state="normal" )
            self.entry_threshold.config( state="normal" )
            self.entry_Csmall.config( state="disabled" )
            self.entry_Cmedium.config( state="disabled" )
            self.entry_Clarge.config( state="disabled" )
            self.entry_small.config( state="disabled" )
            self.entry_medium.config( state="disabled" )
            self.entry_large.config( state="disabled" )
            self.entry_Xlarge.config( state="disabled" )
            self.entry_XXlarge.config( state="disabled" )
            self.entry_thres_Csmall.config( state="disabled" )
            self.entry_thres_Cmedium.config( state="disabled" )
            self.entry_thres_Clarge.config( state="disabled" )
            self.entry_thres_small.config( state="disabled" )
            self.entry_thres_medium.config( state="disabled" )
            self.entry_thres_large.config( state="disabled" )
            self.entry_thres_Xlarge.config( state="disabled" )
            self.entry_thres_XXlarge.config( state="disabled" )
    
    def __update_values( self, e=None ):
        selected = inv_m.Inventory.get_by_name( self.cmbo_item.get() )
        
        if selected.price != selected.staff_price:
            self.staff_price_state.set("normal")
        else:
            self.staff_price_state.set("disabled")
        
        self.txt_price.set( selected.price ), self.txt_staff_price.set( selected.staff_price )
        self.txt_total_stock.set( selected.in_stock ), self.txt_threshold.set( selected.threshold )
        self.catagory.set( selected.catagory )
        
        if selected.catagory == "Clothing":
            self.txt_Csmall.set( selected.sizes[0].in_stock ), self.txt_Cmedium.set( selected.sizes[1].in_stock )
            self.txt_Clarge.set( selected.sizes[2].in_stock ), self.txt_small.set( selected.sizes[3].in_stock )
            self.txt_medium.set( selected.sizes[4].in_stock ), self.txt_large.set( selected.sizes[5].in_stock )
            self.txt_Xlarge.set( selected.sizes[6].in_stock ), self.txt_XXlarge.set( selected.sizes[7].in_stock )
            
            self.thres_Csmall.set( selected.sizes[0].threshold ), self.thres_Cmedium .set( selected.sizes[1].threshold )
            self.thres_Clarge.set( selected.sizes[2].threshold ), self.thres_small.set( selected.sizes[3].threshold )
            self.thres_medium.set( selected.sizes[4].threshold ), self.thres_large.set( selected.sizes[5].threshold )
            self.thres_Xlarge.set( selected.sizes[6].threshold ), self.thres_XXlarge.set( selected.sizes[7].threshold )
        else:
            self.txt_Csmall.set( 0 ), self.txt_Cmedium.set( 0 ), self.txt_Clarge.set( 0 )
            self.txt_small.set( 0 ), self.txt_medium.set( 0 ), self.txt_large.set( 0 )
            self.txt_Xlarge.set( 0 ), self.txt_XXlarge.set( 0 )
            
            self.thres_Csmall.set( 0 ), self.thres_Cmedium .set( 0 ), self.thres_Clarge.set( 0 )
            self.thres_small.set( 0 ), self.thres_medium.set( 0 ), self.thres_large.set( 0 )
            self.thres_Xlarge.set( 0 ), self.thres_XXlarge.set( 0 )
        self.__check_catagory()
        self.__handle_staff_price()
    def __reset_values( self, e=None ):
        self.cmbo_item.set(""), self.txt_price.set( 0 ), self.txt_staff_price.set( 0 )
        self.txt_total_stock.set( 0 ), self.txt_threshold.set( 0 )
        
        self.txt_Csmall.set( 0 ), self.txt_Cmedium.set( 0 ), self.txt_Clarge.set( 0 )
        self.txt_small.set( 0 ), self.txt_medium.set( 0 ), self.txt_large.set( 0 )
        self.txt_Xlarge.set( 0 ), self.txt_XXlarge.set( 0 )
        
        self.thres_Csmall.set( 0 ), self.thres_Cmedium .set( 0 ), self.thres_Clarge.set( 0 )
        self.thres_small.set( 0 ), self.thres_medium.set( 0 ), self.thres_large.set( 0 )
        self.thres_Xlarge.set( 0 ), self.thres_XXlarge.set( 0 )
        self.__update_cmbo()
        self.__check_catagory()
    
    def __on_change( self, *args ):
        try:
            if self.catagory.get() == "Clothing":
                self.txt_total_stock.set(
                    self.txt_Csmall.get() + self.txt_Cmedium.get() + self.txt_Clarge.get() + self.txt_small.get() +
                    self.txt_medium.get() + self.txt_large.get() + self.txt_Xlarge.get() + self.txt_XXlarge.get()
                )
        except:
            pass
    def __on_price_change( self, *args ):
        self.__handle_staff_price()
    def __handle_staff_price( self ):
        self.entry_staff_price.config( state=self.staff_price_state.get() )
        
        try:
            if self.staff_price_state.get() == "disabled":
                self.txt_staff_price.set( self.txt_price.get() )
        except Exception as e:
            print(e)
    
    def save_item( self, e=None ):
        if "|" in self.cmbo_item.get():
            msgbox.showerror("Inventory Name Error", "Inventory item cannot contain '|' character")
            return None
        
        if self.staff_price_state.get() == "disabled":
            self.txt_staff_price.set( self.txt_price.get() )
        
        inv_item = inv_m.Inventory.get_by_name( self.cmbo_item.get() )
        if inv_item is None:
            if self.catagory.get() == "Clothing":
                sizes = [
                    { "size": "C-Small", "in_stock": self.txt_Csmall.get(), "threshold": self.thres_Csmall.get() },
                    { "size": "C-Medium", "in_stock": self.txt_Cmedium.get(), "threshold": self.thres_Cmedium.get() },
                    { "size": "C-Large", "in_stock": self.txt_Clarge.get(), "threshold": self.thres_Clarge.get() },
                    { "size": "Small", "in_stock": self.txt_small.get(), "threshold": self.thres_small.get() },
                    { "size": "Medium", "in_stock": self.txt_medium.get(), "threshold": self.thres_medium.get() },
                    { "size": "Large", "in_stock": self.txt_large.get(), "threshold": self.thres_large.get() },
                    { "size": "X-Large", "in_stock": self.txt_Xlarge.get(), "threshold": self.thres_Xlarge.get() },
                    { "size": "XX-Large", "in_stock": self.txt_XXlarge.get(), "threshold": self.thres_XXlarge.get() }
                ]
            else:
                sizes = []
            inv_m.Inventory.create({
                "name": self.cmbo_item.get(),
                "catagory": self.catagory.get(),
                "in_stock": int(self.txt_total_stock.get()),
                "price": self.txt_price.get(),
                "staff_price": self.txt_staff_price.get(),
                "threshold": int(self.txt_threshold.get()),
                "sizes": sizes
            })
        else:
            if self.catagory.get() == "Clothing":
                sizes = [
                    inv_m.Size({ "size": "C-Small", "in_stock": self.txt_Csmall.get(), "threshold": self.thres_Csmall.get() }),
                    inv_m.Size({ "size": "C-Medium", "in_stock": self.txt_Cmedium.get(), "threshold": self.thres_Cmedium.get() }),
                    inv_m.Size({ "size": "C-Large", "in_stock": self.txt_Clarge.get(), "threshold": self.thres_Clarge.get() }),
                    inv_m.Size({ "size": "Small", "in_stock": self.txt_small.get(), "threshold": self.thres_small.get() }),
                    inv_m.Size({ "size": "Medium", "in_stock": self.txt_medium.get(), "threshold": self.thres_medium.get() }),
                    inv_m.Size({ "size": "Large", "in_stock": self.txt_large.get(), "threshold": self.thres_large.get() }),
                    inv_m.Size({ "size": "X-Large", "in_stock": self.txt_Xlarge.get(), "threshold": self.thres_Xlarge.get() }),
                    inv_m.Size({ "size": "XX-Large", "in_stock": self.txt_XXlarge.get(), "threshold": self.thres_XXlarge.get() })
                ]
            else:
                sizes = []
            inv_item.catagory = self.catagory.get()
            inv_item.in_stock = int(self.txt_total_stock.get())
            inv_item.price = self.txt_price.get()
            inv_item.staff_price = self.txt_staff_price.get()
            inv_item.threshold = int(self.txt_threshold.get())
            inv_item.sizes = sizes
            inv_m.Inventory.update( inv_item.to_dict() )
        
        shop_m.Shopping_List.update({
            "name": self.cmbo_item.get(),
            "in_stock": int(self.txt_total_stock.get()),
            "threshold": int(self.txt_threshold.get()),
        })
        self.__reset_values()
        self.main_window.update_tables()
        self.cmbo.focus()
    
    def delete_item( self, e=None ):
        inv_m.Inventory.delete( self.cmbo_item.get() )
        shop_m.Shopping_List.delete( {"name": self.cmbo_item.get()} )
        self.__reset_values()
        self.main_window.update_tables()
    