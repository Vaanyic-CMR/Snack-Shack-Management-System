from tkinter import *
from tkinter import ttk
from tkinter.font import Font

import math as m

from .. import var_const as vc

from . import (
    settings,
    inventory,
    bank,
    campers,
    staff,
    change_year)

from ..models import (
    history as history_model,
    staff as staff_model,
    camper as camper_model,
    bank as bank_model,
    inventory as inv_model,
    shopping_list as shop_list_model
)

class MainDisplay:
    def __init__( self ):
        # --------------------- Title Bar and General
        self.master = Tk()
        self.master.title("Snack Shack Management System | Admin")
        self.master.iconbitmap("resources/images/logo.ico")
        
        # --------------------- Screen and Window Dimensions
        self.master.state("zoomed")
        self.window_width = self.master.winfo_width()
        self.window_height = self.master.winfo_height()
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        self.master.geometry(f"{int(self.screen_width*0.75)}x{int(self.screen_height*0.75)}")
        
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
        
        s = ttk.Style()
        s.theme_use('vista') # Default is "vista"
        s.configure('TNotebook.Tab', font=self.base_font)
        # s.configure('Treeview', font=self.base_font) # ----- Add Treeview Specifc fonts to settings.
        # s.configure('Treeview.Heading', font=self.base_font)
        s.configure("TCombobox", borderwidth=5 )
        
        # --------------------- General Variables
        self.auto_update_val = IntVar( value=0 )
        self.camp = StringVar( value="Select Camp" )
        
        # --------------------- Table Count Variables.
        self.camper_count = 0
        self.staff_count = 0
        self.history_count = 0
        self.inv_count = 0
        self.shop_list_count = 0
        
        # --------------------- Initialize Base Layout.
        self.__menu_bar()
        
        self.window = ttk.Notebook( self.master )
        self.window.pack( fill=BOTH, expand=1 )
        
        # Sections for personel tab.
        self.tab_1 = Frame( self.window )
        Grid.columnconfigure( self.tab_1, 0, weight=1 )
        Grid.columnconfigure( self.tab_1, 1, weight=1 )
        # Grid.rowconfigure( self.tab_1, 0, weight=1 )
        Grid.rowconfigure( self.tab_1, 1, weight=1 )
        Grid.rowconfigure( self.tab_1, 2, weight=1 )

        self.left_pane = Frame( self.tab_1, 
                            highlightbackground="grey", highlightthickness=1,
                            relief="raised", bd=4)#, bg="black" )
        self.left_pane.grid( row=1, column=0, rowspan=2, sticky="NSWE" )
        self.top_pane = Frame( self.tab_1, 
                            highlightbackground="grey", highlightthickness=1,
                            relief="raised", bd=4)#, bg="red" )
        self.top_pane.grid( row=1, column=1, sticky="NSWE" )
        self.bottom_pane = Frame( self.tab_1, 
                            highlightbackground="grey", highlightthickness=1,
                            relief="raised", bd=4)#, bg="blue" )
        self.bottom_pane.grid( row=2, column=1, sticky="NSWE" )
        
        # Sections for bank/inventory tab.
        self.tab_2 = Frame( self.window )
        Grid.columnconfigure( self.tab_2, 0, weight=1 )
        Grid.columnconfigure( self.tab_2, 1, weight=3 )
        Grid.columnconfigure( self.tab_2, 2, weight=2 )
        Grid.rowconfigure( self.tab_2, 0, weight=1 )
        
        self.bank_pane = Frame( self.tab_2, highlightbackground="grey",
                                highlightthickness=1, relief="raised", bd=4)
        self.bank_pane.grid( row=0, column=0, sticky="NSWE" )
        self.inventory_pane = Frame( self.tab_2, highlightbackground="grey",
                                highlightthickness=1, relief="raised", bd=4)
        self.inventory_pane.grid( row=0, column=1, sticky="NSWE" )
        self.shopping_list_pane = Frame( self.tab_2, highlightbackground="grey",
                                highlightthickness=1, relief="raised", bd=4)
        self.shopping_list_pane.grid( row=0, column=2, sticky="NSWE" )
        
        # Apply Tabs.
        self.window.add( self.tab_1, text="Personel Data" )
        self.window.add( self.tab_2, text="Bank/Inventory Data" )
        
        # Generate Empty Tables
        self.__history_table()
        self.__staff_table()
        self.__camper_table()
        self.__bank_table()
        self.__inventory_table()
        self.__shopping_list_table()
        
        # Fill Tables with data every 10 seconds.
        self.update_tables()
    
    def __open_settings( self ):
        sett = settings.Settings( self )
    def __open_campers( self ):
        c = campers.Campers( self )
    def __open_staff( self ):
        s = staff.Staff( self )
    def __open_inventory( self ):
        i = inventory.Inventory( self )
    def __open_bank( self ):
        b = bank.Bank( self )
    
    def __menu_bar( self ):
        self.menu_bar = Menu( self.master, font=self.base_font )
        self.master.config( menu=self.menu_bar )
        
        # File Menu
        self.file_menu = Menu( self.menu_bar, tearoff=False, font=self.base_font )
        self.file_menu.add_command( label="Exit", command=self.master.quit )
        self.file_menu.add_separator()
        self.file_menu.add_checkbutton(
            label="Auto Update Tables",
            offvalue=0, onvalue=1,
            variable=self.auto_update_val,
            command=self.toggle_auto_update
        )
        self.file_menu.add_command( label="Change Active Year", command=self.change_active_year )
        self.file_menu.add_separator()
        self.file_menu.add_command( label="Manage Campers", command=self.__open_campers )
        self.file_menu.add_command( label="Manage Staff", command=self.__open_staff )
        self.file_menu.add_command( label="Manage Inventory", command=self.__open_inventory )
        self.file_menu.add_command( label="Manage Bank", command=self.__open_bank )
        self.file_menu.add_separator()
        self.file_menu.add_command( label="Export Data | Excel")#, command=AddCommand )
        self.file_menu.add_command( label="Run EOW Check")#, command=AddCommand )
        
        # Options Menu
        self.option_menu = Menu( self.menu_bar, tearoff=False, font=self.base_font )
        self.option_menu.add_command( label="Settings", command=self.__open_settings )
        self.option_menu.add_command( label="About")#, command=AddCommand )
        
        self.menu_bar.add_cascade( label="File", menu=self.file_menu )
        self.menu_bar.add_cascade( label="Options", menu=self.option_menu )
    
    def __history_table( self ):
        headers = ('DateTime', 'Name', 'Purchase Type', '# Items', 'Total')
        
        # History Pane
        Label(self.left_pane, text = "Purchase History", font=self.title_font).pack( side=TOP, fill=X )
        self.history_slider = Scrollbar( self.left_pane, orient=VERTICAL )
        self.history_slider.pack(side=RIGHT, fill=Y)
        self.history_table = ttk.Treeview( self.left_pane, selectmode='browse', yscrollcommand=self.history_slider.set )
        self.history_table.pack(fill=BOTH, expand=1)
        self.history_slider.config(command=self.history_table.yview)

        # History Table
        self.history_table['columns'] = headers
        self.history_table.column('#0', width=20, stretch=NO) # Test Stretch?
        self.history_table.column('DateTime', anchor=W, width=m.floor(self.screen_width/2*0.25))
        self.history_table.column('Name', anchor=CENTER, width=m.floor(self.screen_width/2*0.2))
        self.history_table.column('Purchase Type', anchor=CENTER, width=m.floor(self.screen_width/2*0.2))
        self.history_table.column('# Items', anchor=CENTER, width=m.floor(self.screen_width/2*0.15))
        self.history_table.column('Total', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))

        self.history_table.heading('#0', text='', anchor=W)
        self.history_table.heading('DateTime', text='Date/Time', anchor=W)
        self.history_table.heading('Name', text='Customer Name', anchor=CENTER)
        self.history_table.heading('Purchase Type', text='Purchase Type', anchor=CENTER)
        self.history_table.heading('# Items', text='# of Items', anchor=CENTER)
        self.history_table.heading('Total', text='Total', anchor=CENTER)
    def __staff_table( self ):
        headers = ('Name', 'Last Free Item', '# of Free Items', 'Balance', 'Spent', 'Donations', 'Returned')
        
        # Staff Pane.
        Label(self.top_pane, text = "Staff Data", font=self.title_font).pack(side=TOP, fill=X)
        self.staff_slider = Scrollbar(self.top_pane, orient=VERTICAL)
        self.staff_slider.pack(side=RIGHT, fill=Y)
        self.staff_table = ttk.Treeview(self.top_pane, selectmode='browse', yscrollcommand=self.staff_slider.set)
        # self.staff_table.bind('<Double-1>', lambda event: self.on_click(table = self.staff_table))
        self.staff_table.pack(fill=BOTH, expand=1)
        self.staff_slider.config(command=self.staff_table.yview)

        # Staff Table
        self.staff_table['columns'] = headers
        self.staff_table.column('#0', width=0, stretch=NO)
        self.staff_table.column('Name', anchor=W, width=m.floor(self.screen_width/2*0.15))
        self.staff_table.column('Last Free Item', anchor=CENTER, width=m.floor(self.screen_width/2*0.25))
        self.staff_table.column('# of Free Items', anchor=CENTER, width=m.floor(self.screen_width/2*0.15))
        self.staff_table.column('Balance', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))
        self.staff_table.column('Spent', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))
        self.staff_table.column('Donations', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))
        self.staff_table.column('Returned', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))

        self.staff_table.heading('#0', text='', anchor=W)
        self.staff_table.heading('#1', text='Staff Name', anchor=W)
        self.staff_table.heading('Last Free Item', text='Last Free Item', anchor=CENTER)
        self.staff_table.heading('# of Free Items', text='# of Free Items', anchor=CENTER)
        self.staff_table.heading('Balance', text='Balance', anchor=CENTER)
        self.staff_table.heading('Spent', text='Spent', anchor=CENTER)
        self.staff_table.heading('Donations', text='Donations', anchor=CENTER)
        self.staff_table.heading('Returned', text='Returned', anchor=CENTER)
    def __camper_table( self ):
        headers = ('Name', 'Gender', 'Balance', 'Spent', 'Donations', 'EOW Parent', 'Last Purchase')
        camp_list = [ "Trekker", "Pathfinder", "Journey", "Trail Blazer", "Navigator" ]
        
        # Label(self.bottom_pane, text = "Camper Data", font=self.title_font).pack(side=LEFT)
        camp_menu = OptionMenu( self.bottom_pane, self.camp, *camp_list, command=self.update_tables )
        camp_menu.config( font=self.title_font )
        self.master.nametowidget(camp_menu.menuname).config( font=self.base_font )
        camp_menu.pack(side=TOP)
        
        self.camper_slider = Scrollbar(self.bottom_pane, orient=VERTICAL)
        self.camper_slider.pack(side=RIGHT, fill=Y)
        self.camper_table = ttk.Treeview(self.bottom_pane, selectmode='browse', yscrollcommand=self.camper_slider.set)
        # self.camper_table.bind('<Double-1>', lambda event: self.on_click(table = self.camper_table))
        self.camper_table.pack(fill=BOTH, expand=1)
        self.camper_slider.config(command=self.camper_table.yview)

        # Camper Table
        self.camper_table['columns'] = headers
        self.camper_table.column('#0', width=20, stretch=NO)
        self.camper_table.column('Name', anchor=W, width=m.floor(self.screen_width/2*0.2))
        self.camper_table.column('Gender', anchor=W, width=m.floor(self.screen_width/2*0.1))
        self.camper_table.column('Balance', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))
        self.camper_table.column('Spent', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))
        self.camper_table.column('Donations', anchor=CENTER, width=m.floor(self.screen_width/2*0.1))
        self.camper_table.column('EOW Parent', anchor=CENTER, width=m.floor(self.screen_width/2*0.15))
        self.camper_table.column('Last Purchase', anchor=CENTER, width=m.floor(self.screen_width/2*0.20))

        self.camper_table.heading('#0', text='', anchor=W,
                                    command=self.load_camper_table)
        self.camper_table.heading('Name', text='Camper Name', anchor=W,
                                    command=lambda: self.load_camper_table(sort="name"))
        self.camper_table.heading('Gender', text='Gender', anchor=W,
                                    command=lambda: self.load_camper_table(sort="gender"))
        self.camper_table.heading('Balance', text='Balance', anchor=CENTER,
                                    command=lambda: self.load_camper_table(sort="curr_bal"))
        self.camper_table.heading('Spent', text='Spent', anchor=CENTER,
                                    command=lambda: self.load_camper_table(sort="curr_spent"))
        self.camper_table.heading('Donations', text='Donations', anchor=CENTER,
                                    command=lambda: self.load_camper_table(sort="total_donated"))
        self.camper_table.heading('EOW Parent', text='EOW Parent', anchor=CENTER,
                                    command=lambda: self.load_camper_table(sort="eow_remainder"))
        self.camper_table.heading('Last Purchase', text='Last Purchase', anchor=CENTER,
                                    command=lambda: self.load_camper_table(sort="last_purchase"))
    def __bank_table( self ):
        headers = ('Category', 'Total')
        
        Label(self.bank_pane, text = "Bank Data", font=self.title_font).pack(side=TOP, fill=X)
        self.bank_slider = Scrollbar(self.bank_pane, orient=VERTICAL)
        self.bank_slider.pack(side=RIGHT, fill=Y)
        self.bank_table = ttk.Treeview(self.bank_pane, selectmode='browse', yscrollcommand=self.bank_slider.set)
        self.bank_table.pack(fill=BOTH, expand=1)
        self.bank_slider.config(command=self.bank_table.yview)

        # Bank Table
        self.bank_table['columns'] = headers
        self.bank_table.column('#0', width=0, stretch=NO)
        self.bank_table.column('Category', anchor=W, width=85)
        self.bank_table.column('Total', anchor=CENTER, width=45)

        self.bank_table.heading('#0', text='', anchor=W)
        self.bank_table.heading('Category', text='Category', anchor=W)
        self.bank_table.heading('Total', text='Total', anchor=CENTER)
    def __inventory_table( self ):
        headers = ('Name', 'Catagory', 'In Stock', 'Item Price', 'Low Threshold')
        
        Label(self.inventory_pane, text = "Inventory Data", font=self.title_font).pack(side=TOP, fill=X)
        self.inventory_slider = Scrollbar(self.inventory_pane, orient=VERTICAL)
        self.inventory_slider.pack(side=RIGHT, fill=Y)
        self.inventory_table = ttk.Treeview(self.inventory_pane, selectmode='browse', yscrollcommand=self.inventory_slider.set)
        self.inventory_table.pack(fill=BOTH, expand=1)
        self.inventory_slider.config(command=self.inventory_table.yview)

        # Inventory Table
        self.inventory_table['columns'] = headers
        self.inventory_table.column('#0', width=20, stretch=NO)
        self.inventory_table.column('Name', anchor=W, width=300)
        self.inventory_table.column('Catagory', anchor=CENTER, width=100)
        self.inventory_table.column('In Stock', anchor=CENTER, width=80)
        self.inventory_table.column('Item Price', anchor=CENTER, width=80)
        self.inventory_table.column('Low Threshold', anchor=CENTER, width=90)

        self.inventory_table.heading('#0', text='', anchor=W)
        self.inventory_table.heading('Name', text='Name', anchor=W)
        self.inventory_table.heading('Catagory', text='Catagory', anchor=CENTER)
        self.inventory_table.heading('In Stock', text='In Stock', anchor=CENTER)
        self.inventory_table.heading('Item Price', text='Item Price', anchor=CENTER)
        self.inventory_table.heading('Low Threshold', text='Low Threshold', anchor=CENTER)
    def __shopping_list_table( self ):
        headers = ('Name', 'In Stock', 'Low Threshold', 'Time on List')
        
        Label(self.shopping_list_pane, text = "Shopping List", font=self.title_font).pack(side=TOP, fill=X)
        self.shopping_slider = Scrollbar(self.shopping_list_pane, orient=VERTICAL)
        self.shopping_slider.pack(side=RIGHT, fill=Y)
        self.shopping_table = ttk.Treeview(self.shopping_list_pane, selectmode='browse', yscrollcommand=self.shopping_slider.set)
        self.shopping_table.pack(fill=BOTH, expand=1)
        self.shopping_slider.config(command=self.shopping_table.yview)

        # Shopping List Table
        self.shopping_table['columns'] = headers
        self.shopping_table.column('#0', width=0, stretch=NO)
        self.shopping_table.column('Name', anchor=W, width=200)
        self.shopping_table.column('In Stock', anchor=CENTER, width=80)
        self.shopping_table.column('Low Threshold', anchor=CENTER, width=90)
        self.shopping_table.column('Time on List', anchor=CENTER, width=150)

        self.shopping_table.heading('#0', text='', anchor=W)
        self.shopping_table.heading('Name', text='Name', anchor=W)
        self.shopping_table.heading('In Stock', text='In Stock', anchor=CENTER)
        self.shopping_table.heading('Low Threshold', text='Low Threshold', anchor=CENTER)
        self.shopping_table.heading('Time on List', text='Time on List', anchor=CENTER)
    
    def auto_update( self ):
        self.update_tables()
        if self.auto_update_val.get() == 1:
            self.master.after(10000, self.auto_update)
    def toggle_auto_update( self ):
        self.auto_update()
    
    def update_tables( self, e=None ):
        vc.change_active_camp( self.camp.get().lower() )
        self.load_staff_table()
        self.load_camper_table()
        self.load_bank_table()
        self.load_inventory_table()
        # self.load_shopping_list_table()
        self.load_history_table()
    def change_active_year( self ):
        b = change_year.ChangeYear( self )
    
    def load_history_table( self ):
        # Clear Current Data
        self.history_count = 0
        for r in self.history_table.get_children():
            self.history_table.delete(r)
        
        # Enter New Data
        history_model.History.update_active_database()
        
        data = list()
        try:
            data = history_model.History.get_all()
        except FileNotFoundError:
            if vc.active_camp != "select camp":
                history_model.History.create_file()
                data = history_model.History.get_all()
        
        for d in data:
            info = (d.date_time, d.customer_name, d.purchase_type, len(d.items), d.sum_total)
            
            parent_id = self.history_count
            self.history_table.insert(parent='', index='end', iid=self.history_count, values=info)
            for item in d.items:
                child_info = ("", "", item[0], item[1])
                self.history_count += 1
                self.history_table.insert(parent=f"{parent_id}", index="end", iid=self.history_count, values=child_info)
            self.history_count += 1
    def load_staff_table( self ):
        # Clear Current Data
        self.staff_count = 0
        for r in self.staff_table.get_children():
            self.staff_table.delete(r)
        
        # Enter New Data
        staff_model.Staff.update_active_database()
        
        data = staff_model.Staff.get_all()
        for d in data:
            info = (d.name, d.last_free_item, d.num_of_free_items, d.curr_bal, d.curr_spent, d.total_donated, d.eos_return)
            self.staff_table.insert(parent='', index='end', iid=self.staff_count, values=info)
            self.staff_count += 1
    def load_camper_table( self, e=None, sort=None ):
        # Clear Current Data
        self.camper_count = 0
        for r in self.camper_table.get_children():
            self.camper_table.delete(r)
        
        # Enter New Data
        camper_model.Camper.update_active_database()
        if sort is not None:
            data = camper_model.Camper.get_all_by_camp_sorted_by(
                self.camp.get().lower(), sort )
        else:
            data = camper_model.Camper.get_all_by_camp( self.camp.get().lower() )
        for d in data:
            info = (d.name, d.gender.title(), d.curr_bal, d.curr_spent, d.total_donated, d.eow_remainder.title(), d.last_purchase)
            self.camper_table.insert(parent='', index='end', iid=self.camper_count, values=info)
            self.camper_count += 1
    def load_bank_table( self ):
        # Clear Current Data
        for r in self.bank_table.get_children():
            self.bank_table.delete(r)
        
        # update data in bank fields
        bank_model.Bank.update_fields()
        
        # Enter New Data
        data = bank_model.Bank.get_by_year( vc.active_year )
        self.bank_table.insert(parent='', index='end', iid=0, values=("Bank Total", data.bank_total))
        self.bank_table.insert(parent='', index='end', iid=1, values=("", ""))
        self.bank_table.insert(parent='', index='end', iid=2, values=("Cash Total", data.cash_total))
        self.bank_table.insert(parent='', index='end', iid=3, values=("Check Total", data.check_total))
        self.bank_table.insert(parent='', index='end', iid=4, values=("Card Total", data.card_total))
        self.bank_table.insert(parent='', index='end', iid=5, values=("Scholarship Total", data.scholar_total))
        self.bank_table.insert(parent='', index='end', iid=6, values=("", ""))
        self.bank_table.insert(parent='', index='end', iid=7, values=("Camper Total", data.camper_total))
        self.bank_table.insert(parent='', index='end', iid=8, values=("Staff Total", data.staff_total))
    def load_inventory_table( self ):
        # Clear Current Data
        self.inv_count = 0
        for r in self.inventory_table.get_children():
            self.inventory_table.delete(r)
        # Enter New Data
        data = inv_model.Inventory.get_all()
        for d in data:
            info = (d.name, d.catagory, d.in_stock, d.price, d.threshold)
            if len(d.sizes) > 0:
                parent_id = self.inv_count
                self.inventory_table.insert(parent='', index='end', iid=self.inv_count, values=info)
                for size in d.sizes:
                    child_info = ("        "+size.size, "", size.in_stock, "", size.threshold)
                    self.inv_count += 1
                    self.inventory_table.insert(parent=f"{parent_id}", index="end", iid=self.inv_count, values=child_info)
                self.inv_count += 1
            else:
                self.inventory_table.insert(parent='', index='end', iid=self.inv_count, values=info)
                self.inv_count += 1
    def load_shopping_list_table( self ):
        # Clear Current Data
        self.shop_list_count = 0
        for r in self.shopping_table.get_children():
            self.shopping_table.delete(r)
        
        # Enter New Data
        data = shop_list_model.Shopping_List.get_all()
        for d in data:
            info = (d.name, d.in_stock, d.threshold, d.time_on_list)
            self.shopping_table.insert(parent='', index='end', iid=self.shop_list_count, values=info)
            self.shop_list_count += 1
    