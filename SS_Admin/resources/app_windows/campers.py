from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font

from .. import var_const as vc
from ..models import camper, bank

class Campers:
    def __init__( self, main ):
        self.main_window = main

        # --------------------- Title Bar and General
        self.master = Toplevel()
        self.master.title("SSMS | Campers")
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
        self.active_camper = camper.Camper({
            "rowid": None, "name": "", "gender": "", "camp": "", "pay_method": "",
            "init_bal": 0, "curr_bal": 0, "curr_spent": 0, "total_donated": 0, "eow_return": 0,
            "last_purchase": None, "eow_remainder": "", "created_at": None, "updated_at": None
        })
        self.camp_list = [ "Trekker", "Pathfinder", "Journey", "Trail Blazer", "Navigator" ]
        self.pay_methods = [ "Cash", "Check", "Card", "Scholarship", "Multiple" ]
        self.eow_remainder_options = [ "Unknown", "Return", "Donate", "Transfer" ]
        
        # Form Data Variables
        self.create_update = StringVar( value="create")
        self.create_update.trace('w', self.__update_widgets)
        
        # Camper Data Variables
        self.name = StringVar()
        self.gender = StringVar( value="male")
        self.camp = StringVar( value="Select Camp" )
        self.pay_method = StringVar( value="Select Payment Method" )
        
        self.init_bal = StringVar(value=0)
        self.curr_bal = StringVar(value=0)
        self.curr_spent = StringVar(value=0)
        self.total_donated = StringVar(value=0)
        self.eow_return = StringVar(value=0)
        
        self.last_purchase = StringVar( value="Month, day Year | 00:00:00 pm" )
        
        self.eow_remainder = StringVar( value="Select Action" )
        
        # ----- Frames
        self.north_frame = Frame( self.master, padx=10, pady=10 )
        self.north_frame.grid( row=0, column=0 )
        
        central_frame = Frame( self.master, padx=10, pady=10 )
        central_frame.grid( row=2, column=0 )
        
        self.west_frame = Frame( central_frame, padx=10, pady=10 )
        self.west_frame.pack( side=LEFT, fill=BOTH, expand=True )
        ttk.Separator( central_frame, orient="vertical" ).pack( side=LEFT, fill=BOTH, expand=True, padx=10 )
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
        rd_create.grid( row=0, column=0 )
        
        camp_menu = OptionMenu( self.north_frame, self.camp, *self.camp_list, command=self.__update_name_cmbo )
        camp_menu.config( font=self.base_font )
        self.master.nametowidget(camp_menu.menuname).config( font=self.base_font )
        camp_menu.grid( row=0, column=1 )
        
        rd_update = Radiobutton( self.north_frame, text="Update", font=self.base_font, variable=self.create_update, value="update" )
        rd_update.grid( row=0, column=2 )
    def __build_west_frame( self ):
        Label( self.west_frame, text="Name:", font=self.base_font ).grid( row=0, column=0, columnspan=3 )
        self.name_cmbo = ttk.Combobox( self.west_frame, textvariable=self.name, font=self.base_font )
        self.name_cmbo.bind( "<<ComboboxSelected>>", self.__update_content )
        self.name_cmbo.bind( "<Return>", self.save_camper )
        self.name_cmbo.bind( "<Shift-Return>", self.delete_camper )
        self.name_cmbo.grid( row=1, column=0, columnspan=3 )
        
        Label( self.west_frame, text="Gender:", font=self.base_font ).grid( row=2, column=0 )
        rd_male = Radiobutton( self.west_frame, text="Male", font=self.base_font, variable=self.gender, value="male" )
        rd_male.grid( row=2, column=1 )
        rd_female = Radiobutton( self.west_frame, text="Female", font=self.base_font, variable=self.gender, value="female" )
        rd_female.grid( row=2, column=2 )
        
        Label( self.west_frame, text="Payment Method", font=self.base_font ).grid( row=3, column=0, columnspan=3 )
        pay_method_opt = OptionMenu( self.west_frame, self.pay_method, *self.pay_methods )
        pay_method_opt.config( font=self.base_font )
        self.master.nametowidget(pay_method_opt.menuname).config( font=self.base_font )
        pay_method_opt.grid( row=4, column=0, columnspan=3 )
    def __build_east_frame( self ):
        Label( self.east_frame, text="Initial Balance", font=self.base_font ).grid( row=0, column=0 )
        self.init_bal_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.init_bal, font=self.base_font )
        self.init_bal_entry.bind( "<Return>", self.save_camper )
        self.init_bal_entry.bind( "<Shift-Return>", self.delete_camper )
        self.init_bal_entry.grid( row=1, column=0 )
        
        Label( self.east_frame, text="Current Balance", font=self.base_font ).grid( row=0, column=1 )
        self.curr_bal_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.curr_bal, font=self.base_font )
        self.curr_bal_entry.bind( "<Return>", self.save_camper )
        self.curr_bal_entry.bind( "<Shift-Return>", self.delete_camper )
        self.curr_bal_entry.grid( row=1, column=1 )
        
        Label( self.east_frame, text="Current Spent", font=self.base_font ).grid( row=2, column=0 )
        self.spent_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.curr_spent, font=self.base_font )
        self.spent_entry.bind( "<Return>", self.save_camper )
        self.spent_entry.bind( "<Shift-Return>", self.delete_camper )
        self.spent_entry.grid( row=3, column=0 )
        
        Label( self.east_frame, text="Donations", font=self.base_font ).grid( row=2, column=1 )
        self.donation_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.total_donated, font=self.base_font )
        self.donation_entry.bind( "<Return>", self.save_camper )
        self.donation_entry.bind( "<Shift-Return>", self.delete_camper )
        self.donation_entry.grid( row=3, column=1 )
        
        Label( self.east_frame, text="EOW Returns", font=self.base_font ).grid( row=4, column=0, columnspan=2 )
        self.return_entry = Entry( self.east_frame, borderwidth=5, textvariable=self.eow_return, font=self.base_font )
        self.return_entry.bind( "<Return>", self.save_camper )
        self.return_entry.bind( "<Shift-Return>", self.delete_camper )
        self.return_entry.grid( row=5, column=0, columnspan=2 )
        
        Label( self.east_frame, text="Last Purchase", font=self.base_font ).grid( row=6, column=0 )
        Label( self.east_frame, text=self.last_purchase.get(), font=self.base_font ).grid( row=7, column=0 )
        
        Label( self.east_frame, text="EOW Remaining", font=self.base_font ).grid( row=6, column=1 )
        eow_remaining = OptionMenu( self.east_frame, self.eow_remainder, *self.eow_remainder_options )
        eow_remaining.config( font=self.base_font )
        self.master.nametowidget(eow_remaining.menuname).config( font=self.base_font )
        eow_remaining.grid( row=7, column=1 )
    def __build_south_frame( self ):
        Button( self.south_frame, text="Save\n(Return)", font=self.base_font, command=self.save_camper, padx=20
            ).grid( row=0, column=0, padx=30 )
        Button( self.south_frame, text="Delete\n(Shift+Return)", font=self.base_font, command=self.delete_camper, padx=20
            ).grid( row=0, column=1, padx=30 )
    
    def __update_name_cmbo( self, e=None ):
        if self.create_update.get() == "update":
            self.ids_names = camper.Camper.get_all_names_by_camp( self.camp.get().lower() )
            self.name_cmbo.config( value=self.ids_names )
        else:
            self.name.set("")
            self.__reset_name_cmbo()
    def __reset_name_cmbo( self, e=None ):
        self.name_cmbo.config( value=[] )
    
    def __reset_content( self, e=None ):
        self.name.set("")
        self.pay_method.set( "Select Payment Method" )
        self.init_bal.set(0)
        self.curr_bal.set(0)
        self.curr_spent.set(0)
        self.total_donated.set(0)
        self.eow_return.set(0)
        self.last_purchase.set( "Month, day Year | 00:00:00 pm" )
        self.eow_remainder.set("Select Action")
    def __update_content( self, e=None ):
        if self.create_update.get() == "update":
            self.active_camper = camper.Camper.get_by_name_and_camp(
                self.name.get(),
                self.camp.get().lower()
            )
            self.gender.set( self.active_camper.gender )
            self.pay_method.set( self.active_camper.pay_method.title() )
            self.init_bal.set( self.active_camper.init_bal )
            self.curr_bal.set( self.active_camper.curr_bal )
            self.curr_spent.set( self.active_camper.curr_spent )
            self.total_donated.set( self.active_camper.total_donated )
            self.eow_return.set( self.active_camper.eow_return )
            self.last_purchase.set( self.active_camper.last_purchase )
            self.eow_remainder.set( self.active_camper.eow_remainder.title() )
    
    # Runs when Create/Update Radiobuttons change.
    def __update_widgets( self, *aargs ):
        if self.create_update.get() == "create":
            self.__disable_widgets()
        elif self.create_update.get() == "update":
            self.__enable_widgets()
        else:
            print("Error: Variable self.create_update has invalid value:", self.create_update.get() )
    def __enable_widgets( self ):
        self.curr_bal_entry.config( state="normal" )
        self.spent_entry.config( state="normal" )
        self.donation_entry.config( state="normal" )
        self.return_entry.config( state="normal" )
        self.__update_name_cmbo()
    def __disable_widgets( self ):
        self.curr_bal_entry.config( state="disabled" )
        self.spent_entry.config( state="disabled" )
        self.donation_entry.config( state="disabled" )
        self.return_entry.config( state="disabled" )
        self.last_purchase.set( "00-00-00 00:00:00" )
        self.eow_remainder.set("Select Action")
        
        self.__reset_name_cmbo()
        self.__reset_content()
    
    def __create_camper( self ):
        self.active_camper.curr_bal = float(self.init_bal.get())
        camper.Camper.create( self.active_camper.to_dict() )
        
        bnk = bank.Bank.get_by_year( vc.active_year )
        bnk.bank_total += float(self.init_bal.get())
        bnk.camper_total += float(self.init_bal.get())
        if self.pay_method.get() == "Cash":
            bnk.account_cash_total += float(self.init_bal.get())
        elif self.pay_method.get() == "Check":
            bnk.account_check_total += float(self.init_bal.get())
        elif self.pay_method.get() == "Card":
            bnk.account_card_total += float(self.init_bal.get())
        elif self.pay_method.get() == "Scholarship":
            bnk.account_scholar_total += float(self.init_bal.get())
        
        bank.Bank.save( bnk.to_dict() )
    def __update_camper( self ):
        bnk = bank.Bank.get_by_year( vc.active_year )
        updating_camper = camper.Camper.get_by_name_and_camp(
            self.name.get(), self.camp.get().lower()
        )
        
        bnk.bank_total += self.active_camper.init_bal - updating_camper.init_bal
        bnk.donation_total += self.active_camper.total_donated - updating_camper.total_donated
        bnk.camper_total += self.active_camper.init_bal - updating_camper.init_bal
        if self.pay_method.get() == "cash":
            bnk.account_cash_total += self.active_camper.init_bal - updating_camper.init_bal
        elif self.pay_method.get() == "check":
            bnk.account_check_total += self.active_camper.init_bal - updating_camper.init_bal
        elif self.pay_method.get() == "card":
            bnk.account_card_total += self.active_camper.init_bal - updating_camper.init_bal
        elif self.pay_method.get() == "scholarship":
            bnk.account_scholar_total += self.active_camper.init_bal - updating_camper.init_bal
        
        bank.Bank.save( bnk.to_dict() )
        camper.Camper.update( self.active_camper.to_dict() )
    def delete_camper( self, e=None ):
        bnk = bank.Bank.get_by_year( vc.active_year )
        
        bnk.bank_total -= float(self.init_bal.get())
        bnk.donation_total -= float(self.total_donated.get())
        bnk.camper_total -= float(self.init_bal.get())
        if self.pay_method.get() == "cash":
            bnk.account_cash_total -= float(self.init_bal.get())
        elif self.pay_method.get() == "check":
            bnk.account_check_total -= float(self.init_bal.get())
        elif self.pay_method.get() == "card":
            bnk.account_card_total -= float(self.init_bal.get())
        elif self.pay_method.get() == "scholarship":
            bnk.account_scholar_total -= float(self.init_bal.get())
        
        try:
            camper.Camper.delete( self.active_camper.id )
            bank.Bank.save( bnk.to_dict() )
            self.__reset_content()
            self.__update_name_cmbo()
            self.main_window.update_tables()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")
    def save_camper( self, e=None ):
        if self.camp.get().lower() not in [ "trekker", "pathfinder", "journey", "trail blazer", "navigator" ]:
            messagebox.showerror("Value Error", "Invalid camp selected")
            return None
        if self.eow_remainder.get() == "Select Action":
            messagebox.showerror("Error", "Please select an 'End of Week' action.")
            return None
        
        self.active_camper.name = self.name.get()
        self.active_camper.gender = self.gender.get()
        self.active_camper.camp = self.camp.get().lower()
        self.active_camper.pay_method = self.pay_method.get().lower()
        self.active_camper.init_bal = float(self.init_bal.get())
        self.active_camper.curr_bal = float(self.curr_bal.get())
        self.active_camper.curr_spent = float(self.curr_spent.get())
        self.active_camper.total_donated = float(self.total_donated.get())
        self.active_camper.eow_return = float(self.eow_return.get())
        self.active_camper.last_purchase = self.last_purchase.get()
        self.active_camper.eow_remainder = self.eow_remainder.get().lower()
        
        if self.create_update.get() == "create":
            self.__create_camper()
        elif self.create_update.get() == "update":
            self.__update_camper()
        else:
            print("Error: Variable self.create_update has invalid value:", self.create_update.get() )
        
        self.__reset_content()
        self.__update_name_cmbo()
        self.main_window.update_tables()
    