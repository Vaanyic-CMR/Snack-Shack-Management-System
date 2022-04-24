from tkinter import *
from tkinter import ttk
from tkinter.font import Font

from .sub_components import transaction_row as tr

from .. import (
    var_const as vc,
    client
)

class CamperTransactions:
    def __init__(self) -> None:
        # --------------------- Title Bar and General
        self.master = Tk()
        self.master.title("Snack Shack Management System | Register")
        self.master.iconbitmap("resources/images/logo.ico")
        self.master.config( bg="light grey" )
        self.master.state("zoomed")
        
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
        self.master.option_add('*TCombobox*Listbox.font', self.base_font)
        
        s = ttk.Style()
        s.theme_use('xpnative') # Default is "vista"
        s.configure('TNotebook.Tab', font=self.base_font)
        s.configure("TCombobox", darkcolor="grey", lightcolor="grey" )
        
        # ----- Declaring tk Variables
        self.gender = StringVar(value="Select Gender")
        self.camper_name = StringVar()
        
        self.account_total = StringVar(value="${:,.2f}".format(0)) # use "${:,.2f}".format(val) to format
        self.sum_total = StringVar(value="${:,.2f}".format(0))
        self.donation = StringVar(value="${:,.2f}".format(0))
        self.returns = StringVar(value="${:,.2f}".format(0))
        self.remaining_balance = StringVar(value="${:,.2f}".format(0))
        
        self.food_limit = StringVar(value="${:,.2f}".format(0) + "/${:,.2f}".format(vc.settings.food_limit))
        
        # ----- Initializing Frames
        self.header_frame = Frame( self.master, relief="ridge", borderwidth=5 )
        self.header_frame.pack( fill=X )
        self.body_frame = Frame( self.master )
        self.body_frame.pack( fill=BOTH, expand=True, pady=10 )
        self.footer_frame = Frame( self.master, relief="ridge", borderwidth=5 )
        self.footer_frame.pack( fill=X )#.place( relwidth=1, relx=0.5, rely=1, anchor=S )
        
        # ----- Variables
        self.rows = list()
        self.camper_names = list()
        self.inventory_names = list()
        
        # ----- Constructing main builds
        self.__menu_bar()
        self.__build_header()
        self.__build_body()
        self.__build_footer()
        
        # Add a row of transaction items.
        self.__add_row()
        
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
    # ---------------------- Construct Menu Bar
    def __menu_bar( self ):
        self.t_menu = Menu(self.master)
        self.master.config(menu=self.t_menu, padx=20, pady=20)

        # File Menu
        self.file_menu = Menu(self.t_menu, tearoff = False)
        self.t_menu.add_cascade(label='File', menu = self.file_menu)
        self.file_menu.add_command(label='Exit', command = self.master.destroy)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Reload Inventory', command = self.__reload_inventory)
        self.file_menu.add_command(label='Reload Camper Names', command = self.__update_cmbobox)

        # Options Menu
        self.option_menu = Menu(self.t_menu, tearoff=False)
        self.t_menu.add_cascade(label='Options', menu=self.option_menu)
        self.option_menu.add_command(label='Settings')#, command=self.openSettings)
        self.option_menu.add_command(label='About')#, command=self.openAbout)
    
    # ---------------------- Contruct Components
    def __build_header( self ):
        Label(self.header_frame, text = "Camper Transactions", font = self.title_font
            ).pack(side=LEFT, padx=15, pady=5)
        
        genders = ["Male", "Female"]
        gender_menu = OptionMenu( self.header_frame, self.gender, *genders, command=self.__update_cmbobox )
        gender_menu.config( font=self.base_font )
        self.master.nametowidget(gender_menu.menuname).config( font=self.base_font )
        gender_menu.pack(side=LEFT, padx=5, pady=5)
        
        self.cmbo_name = ttk.Combobox( self.header_frame, font=self.base_font,
            textvariable=self.camper_name
        )
        # self.cmbo_name.set_completion_list(self.names)
        # self.cmbo_name.bind('<<ComboboxSelected>>', self.update)
        self.cmbo_name.pack(side=LEFT, padx=5, pady=5)
        self.cmbo_name.focus()
        
        # Cash Button
        self.btnCash = Button(self.header_frame, text="Cash", width=10,
                            borderwidth=5, font=self.base_font)#, command = self.openCash)
        self.btnCash.pack(side=RIGHT, padx=5, pady=5)
        # Staff Button
        self.btnStaff = Button(self.header_frame, text="Staff", width=10,
                            borderwidth=5, font=self.base_font)#, command = self.openStaff)
        self.btnStaff.pack(side=RIGHT, padx=5, pady=5)
    def __build_body( self ):
        body_canvas = Canvas( self.body_frame )
        body_canvas.pack( side=LEFT, fill=BOTH, expand=True )
        body_scrollbar = ttk.Scrollbar( self.body_frame , orient=VERTICAL, command=body_canvas.yview )
        body_scrollbar.pack( side=RIGHT, fill=Y )
        
        # Configure Canvas
        body_canvas.configure( yscrollcommand=body_scrollbar.set )
        body_canvas.bind( '<Configure>',
            lambda e: body_canvas.configure(scrollregion=body_canvas.bbox("all")) )
        
        # New canvas frame
        self.canvas_frame = Frame( body_canvas )
        body_canvas.create_window((0,0), window=self.canvas_frame, anchor=NW )
    def __add_row( self ):
        self.rows.append(
            tr.TransactionRow(
                frame=self.canvas_frame,
                data=Row(),
                on_update=self.update_values
            )
        )
        self.__load_inventory_names()
        for idx, row in enumerate(self.rows):
            self.rows[idx].populate_listboxes(self.inventory_names)
    def __build_footer( self ):
        Label(self.footer_frame, text="Total In Account", font=self.base_font
            ).grid(row=0, column=0, padx=5)
        Label(self.footer_frame, textvariable=self.account_total, font=self.base_font
            ).grid(row=1, column=0, padx=5)

        Label(self.footer_frame, text="Total Item Price", font=self.base_font
            ).grid(row=0, column=1, padx=10, pady=10)
        Label(self.footer_frame, textvariable=self.sum_total, font=self.base_font
            ).grid(row=1, column=1, padx=5)

        Label(self.footer_frame, text="Donation", font=self.base_font
            ).grid(row=0, column=2, padx=5)
        Label(self.footer_frame, textvariable=self.donation, font=self.base_font
            ).grid(row=1, column=2, padx=5)

        Label(self.footer_frame, text="Returns", font=self.base_font
            ).grid(row=0, column=3, padx=5)
        Label(self.footer_frame, textvariable=self.returns, font=self.base_font
            ).grid(row=1, column=3, padx=5)

        Label(self.footer_frame, text="Remaining Balance", font=self.base_font
            ).grid(row=0, column=4, padx=5)
        Label(self.footer_frame, textvariable=self.remaining_balance, font=self.base_font
            ).grid(row=1, column=4, padx=5)

        # Footer Right side
        Button(self.footer_frame, text="Add Row", font=self.base_font,
            borderwidth=5, padx=10, command=self.__add_row
        ).grid(row=0, column=6, rowspan=2, padx=5, pady=5)
        
        Button(self.footer_frame, text="Return", font=self.base_font,
            width=10, borderwidth=5, padx=10,# command=self.__donation
        ).grid(row=0, column=7, padx=5, pady=5)
        Button(self.footer_frame, text="Donation", font=self.base_font,
            width=10, borderwidth=5, padx=10,# command=self.__donation
        ).grid(row=1, column=7, padx=5, pady=5)
        
        Button(self.footer_frame, text="Complete Transaction", font=self.base_font,
            width=25, borderwidth=5#, command = self.complete_transaction
        ).grid(row=0, column=8, padx=5, pady=5)
        Label(self.footer_frame, fg = 'black', font=self.base_font,
            text = f"Food Limit: $0.00/${vc.settings.food_limit}"
        ).grid(row=1, column=8, padx=5, pady=5)
        
        # configure colume to seperate left and right
        Grid.columnconfigure(self.footer_frame, 5, weight=1)

    # ---------------------- Retrieving and displaying data
    # ----- Inventory Data
    def __load_inventory_names( self ):
        cmd = ("api/inventory/names", None)
        client.send( cmd )
        self.inventory_names = client.response_from_server()
        pass
    def __reload_inventory( self ):
        pass
    # ----- Camper Data
    def __update_cmbobox( self, e=None ):
        cmd = ("api/campers/names", self.gender.get().lower())
        client.send( cmd )
        self.camper_names = client.response_from_server()
        self.cmbo_name.config( value=self.camper_names )
    def update_values( self, e=None ):
        # val = self.rows[0].data.col1["spinbox_val"].get()
        # print(f"Col 1: {val}")
        pass

class Row:
    def __init__(self) -> None:
        self.col1 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar()
        }
        self.col2 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar()
        }
        self.col3 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar()
        }
        self.col4 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar()
        }
        self.col5 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar()
        }