from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox

from .. import var_const as vc
from ..models import staff, bank

class Staff:
    def __init__( self, main ):
        self.main_window = main

        # --------------------- Title Bar and General
        self.master = Toplevel()
        self.master.title("SSMS | Staff")
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
        
        # ----- Variables
        self.active_staff = staff.Staff({
            "rowid": None, "name": "", "pay_method": "", "num_of_free_items": 0, "last_free_item": None,
            "init_bal": 0, "curr_bal": 0, "curr_spent": 0, "total_donated": 0, "eos_return": 0,
            "last_purchase": None, "created_at": None, "updated_at": None
        })
        self.pay_methods = [ "None", "Cash", "Check", "Card", "Scholarship"]#, "Multiple" ]
        
        # Form Data Variables
        self.create_update = StringVar( value="create")
        self.create_update.trace('w', self.__update_widgets)
        
        # Staffer Data Variables
        self.name = StringVar()
        self.pay_method = StringVar( value="Select Payment Method" )
        self.num_of_free_items = IntVar()
        self.last_free_item = StringVar( value="Month, day Year | 00:00:00 pm" )
        
        self.init_bal = StringVar()
        self.curr_bal = StringVar()
        self.curr_spent = StringVar()
        self.total_donated = StringVar()
        self.eos_return = StringVar()
        
        self.last_purchase = StringVar( value="Month, day Year | 00:00:00 pm" )
        
        # ----- Frames
        # Contains self.create_update and self.name
        self.north_frame = Frame( self.master, padx=10, pady=10 )
        self.north_frame.grid( row=0, column=0 )
        
        # Contains self.west_frame and self.east_frame
        central_frame = Frame( self.master, padx=10, pady=10 )
        central_frame.grid( row=2, column=0 )
        
        # Contains self.pay_method, self.num_of_free_items, and self.last_free_item
        self.west_frame = Frame( central_frame, padx=10, pady=10 )
        self.west_frame.pack( side=LEFT, fill=BOTH, expand=True )
        
        ttk.Separator( central_frame, orient="vertical" ).pack( side=LEFT, fill=BOTH, expand=True, padx=10 )
        
        # Contains bank info
        self.east_frame = Frame( central_frame, padx=10, pady=10 )
        self.east_frame.pack( side=RIGHT, fill=BOTH, expand=True )
        
        self.south_frame = Frame( self.master, padx=10, pady=10 )
        self.south_frame.grid( row=3, column=0 )
        
        # ----- Building Content
        self.__build_north_frame()
        self.__build_west_frame()
        self.__build_east_frame()
        self.__build_south_frame()
        self.__set_geometery()
        
        # ----- Prepopulating content
        self.__update_widgets()
    
    # --------------------- Screen and Window Dimensions
    def __set_geometery( self ):
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.window_width = int( self.screen_width*0.30 )
        self.window_height = int( self.screen_height*0.30 )
        
        self.window_position_x = int( self.screen_width/2 - self.window_width/2 )
        self.window_position_y = int( self.screen_height/2 - self.window_height/2 )
        
        self.master.geometry( f"+{ self.window_position_x }+{ self.window_position_y }" )
    
    def __build_north_frame( self ):
        rd_create = Radiobutton( self.north_frame, text="Create", font=self.base_font, variable=self.create_update, value="create" )
        rd_create.grid( row=0, column=0, rowspan=2, padx=10 )
        
        Label( self.north_frame, text="Name:", font=self.base_font ).grid( row=0, column=1 )
        self.name_cmbo = ttk.Combobox( self.north_frame, textvariable=self.name, font=self.base_font )
        self.name_cmbo.bind( "<<ComboboxSelected>>", self.__update_content )
        self.name_cmbo.bind( "<Return>", self.save_staffer )
        self.name_cmbo.bind( "<Shift-Return>", self.delete_staffer )
        self.name_cmbo.grid( row=1, column=1 )
        
        rd_update = Radiobutton( self.north_frame, text="Update", font=self.base_font, variable=self.create_update, value="update" )
        rd_update.grid( row=0, column=2, rowspan=2, padx=10 )
    def __build_west_frame( self ):
        Label( self.west_frame, text="Payment Method", font=self.base_font ).grid( row=0, column=0 )
        pay_method_opt = OptionMenu( self.west_frame, self.pay_method, *self.pay_methods )
        pay_method_opt.config( font=self.base_font )
        self.master.nametowidget(pay_method_opt.menuname).config( font=self.base_font )
        pay_method_opt.grid( row=1, column=0 )
        
        Label( self.west_frame, text="# of free items recieved.", font=self.base_font ).grid( row=2, column=0 )
        self.num_free = Entry( self.west_frame, borderwidth=5, textvariable=self.num_of_free_items, font=self.base_font )
        self.num_free.bind( "<Return>", self.save_staffer )
        self.num_free.bind( "<Shift-Return>", self.delete_staffer )
        self.num_free.grid( row=3, column=0 )
        
        Label( self.west_frame, text="Last free item.", font=self.base_font ).grid( row=4, column=0 )
        Label( self.west_frame, text=self.last_free_item.get(), font=self.base_font ).grid( row=5, column=0 )
    def __build_east_frame( self ):
        Label( self.east_frame, text="Initial Balance", font=self.base_font ).grid( row=0, column=0 )
        init_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.init_bal, font=self.base_font )
        init_entry.bind( "<Return>", self.save_staffer )
        init_entry.bind( "<Shift-Return>", self.delete_staffer )
        init_entry.grid( row=1, column=0 )
        
        Label( self.east_frame, text="Current Balance", font=self.base_font ).grid( row=2, column=0 )
        self.curr_bal_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.curr_bal, font=self.base_font )
        self.curr_bal_entry.bind( "<Return>", self.save_staffer )
        self.curr_bal_entry.bind( "<Shift-Return>", self.delete_staffer )
        self.curr_bal_entry.grid( row=3, column=0 )
        
        Label( self.east_frame, text="Current Spent", font=self.base_font ).grid( row=4, column=0 )
        self.spent_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.curr_spent, font=self.base_font )
        self.spent_entry.bind( "<Return>", self.save_staffer )
        self.spent_entry.bind( "<Shift-Return>", self.delete_staffer )
        self.spent_entry.grid( row=5, column=0 )
        
        Label( self.east_frame, text="Total Donated", font=self.base_font ).grid( row=0, column=1 )
        self.donation_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.total_donated, font=self.base_font )
        self.donation_entry.bind( "<Return>", self.save_staffer )
        self.donation_entry.bind( "<Shift-Return>", self.delete_staffer )
        self.donation_entry.grid( row=1, column=1 )
        
        Label( self.east_frame, text="Returned End of Season", font=self.base_font ).grid( row=2, column=1 )
        self.return_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.eos_return, font=self.base_font )
        self.return_entry.bind( "<Return>", self.save_staffer )
        self.return_entry.bind( "<Shift-Return>", self.delete_staffer )
        self.return_entry.grid( row=3, column=1 )
        
        Label( self.east_frame, text="Last Purchase:", font=self.base_font ).grid( row=4, column=1 )
        Label( self.east_frame, text=self.last_purchase.get(), font=self.base_font ).grid( row=5, column=1 )
    def __build_south_frame( self ):
        Button( self.south_frame, text="Save Item\n(Return)", font=self.base_font, command=self.save_staffer, padx=20
            ).grid( row=0, column=0, padx=30 )
        Button( self.south_frame, text="Delete Item\n(Shift+Return)", font=self.base_font, command=self.delete_staffer, padx=20
            ).grid( row=0, column=1, padx=30 )
    
    # --------------------- Update Widgets
    def __update_widgets( self, *aargs ):
        if self.create_update.get() == "create":
            self.__disable_widgets()
        elif self.create_update.get() == "update":
            self.__enable_widgets()
        else:
            print("Error: Variable self.create_update has invalid value:", self.create_update.get() )
    def __enable_widgets( self ):
        self.num_free.config( state="normal" )
        self.curr_bal_entry.config( state="normal" )
        self.spent_entry.config( state="normal" )
        self.donation_entry.config( state="normal" )
        self.return_entry.config( state="normal" )
        self.__update_name_cmbo()
    def __disable_widgets( self ):
        self.num_free.config( state="disabled" )
        self.curr_bal_entry.config( state="disabled" )
        self.spent_entry.config( state="disabled" )
        self.donation_entry.config( state="disabled" )
        self.return_entry.config( state="disabled" )
        self.last_purchase.set( "00-00-00 00:00:00" )
        
        self.__reset_name_cmbo()
        self.__reset_content()
    
    # --------------------- Change Values of Widgets
    def __update_name_cmbo( self, e=None ):
        if self.create_update.get() == "update":
            ids_names = staff.Staff.get_all_names()
            self.name_cmbo.config( value=ids_names )
        else:
            self.name.set("")
            self.__reset_name_cmbo()
    def __reset_name_cmbo( self, e=None ):
        self.name_cmbo.config( value=[] )
    def __update_content( self, e=None ):
        if self.create_update.get() == "update":
            self.active_staff = staff.Staff.get_by_name( self.name.get())
            self.pay_method.set( self.active_staff.pay_method )
            self.num_of_free_items.set( self.active_staff.num_of_free_items )
            self.last_free_item.set( self.active_staff.last_free_item )
            
            self.init_bal.set( self.active_staff.init_bal )
            self.curr_bal.set( self.active_staff.curr_bal )
            self.curr_spent.set( self.active_staff.curr_spent )
            self.total_donated.set( self.active_staff.total_donated )
            self.eos_return.set( self.active_staff.eos_return )
            self.last_purchase.set( self.active_staff.last_purchase )
    def __reset_content( self ):
        self.name.set("")
        self.pay_method.set( "Select Payment Method" )
        self.num_of_free_items.set(0)
        self.last_free_item.set( "00-00-00 00:00:00" )
        
        self.init_bal.set(0)
        self.curr_bal.set(0)
        self.curr_spent.set(0)
        self.total_donated.set(0)
        self.eos_return.set(0)
        self.last_purchase.set( "00-00-00 00:00:00" )
    
    # ---------------------- Write to Database
    def save_staffer( self, e=None ):
        self.active_staff.name = self.name.get()
        self.active_staff.pay_method = self.pay_method.get().lower()
        self.active_staff.num_of_free_items = self.num_of_free_items.get()
        self.active_staff.last_free_item = self.last_free_item.get()
        
        self.active_staff.init_bal = float(self.init_bal.get())
        self.active_staff.curr_bal = float(self.curr_bal.get())
        self.active_staff.curr_spent = float(self.curr_spent.get())
        self.active_staff.total_donated = float(self.total_donated.get())
        self.active_staff.eos_return = float(self.eos_return.get())
        
        self.active_staff.last_purchase = self.last_purchase.get()
        
        if self.create_update.get() == "create":
            self.__create()
        elif self.create_update.get() == "update":
            self.__update()
        else:
            print("Error: Variable self.create_update has invalid value:", self.create_update.get() )
        
        self.__update_name_cmbo()
        self.main_window.update_tables()
    def delete_staffer( self, e=None ):
        bnk = bank.Bank.get_by_year( vc.active_year )
        
        bnk.bank_total -= float(self.init_bal.get())
        bnk.donation_total -= float(self.total_donated.get())
        bnk.staff_total -= float(self.init_bal.get())
        if self.pay_method.get() == "cash":
            bnk.account_cash_total -= float(self.init_bal.get())
        elif self.pay_method.get() == "check":
            bnk.account_check_total -= float(self.init_bal.get())
        elif self.pay_method.get() == "card":
            bnk.account_card_total -= float(self.init_bal.get())
        elif self.pay_method.get() == "scholarship":
            bnk.account_scholar_total -= float(self.init_bal.get())
        
        try:
            staff.Staff.delete( self.name.get() )
            bank.Bank.save( bnk.to_dict() )
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")
    def __update( self ):
        bnk = bank.Bank.get_by_year( vc.active_year )
        updating_staff = staff.Staff.get_by_name( self.name.get() )
        
        bnk.bank_total += self.active_staff.init_bal - updating_staff.init_bal
        bnk.donation_total += self.active_staff.total_donated - updating_staff.total_donated
        bnk.staff_total += self.active_staff.init_bal - updating_staff.init_bal
        if self.pay_method.get() == "cash":
            bnk.account_cash_total += self.active_staff.init_bal - updating_staff.init_bal
        elif self.pay_method.get() == "check":
            bnk.account_check_total += self.active_staff.init_bal - updating_staff.init_bal
        elif self.pay_method.get() == "card":
            bnk.account_card_total += self.active_staff.init_bal - updating_staff.init_bal
        elif self.pay_method.get() == "scholarship":
            bnk.account_scholar_total += self.active_staff.init_bal - updating_staff.init_bal
        
        bank.Bank.save( bnk.to_dict() )
        staff.Staff.update( self.active_staff.to_dict() )
        self.__reset_content()
    def __create( self ):
        self.active_staff.curr_bal = float(self.init_bal.get())
        staff.Staff.create( self.active_staff.to_dict() )
        
        bnk = bank.Bank.get_by_year( vc.active_year )
        bnk.bank_total += float(self.init_bal.get())
        bnk.camper_total += float(self.init_bal.get())
        if self.pay_method.get() == "cash":
            bnk.account_cash_total += float(self.init_bal.get())
        elif self.pay_method.get() == "check":
            bnk.account_check_total += float(self.init_bal.get())
        elif self.pay_method.get() == "card":
            bnk.account_card_total += float(self.init_bal.get())
        elif self.pay_method.get() == "scholarship":
            bnk.account_scholar_total += float(self.init_bal.get())
        
        self.__reset_content()
    
    