from datetime import datetime
import time

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font

from .sub_components import (
    transaction_row as tr,
    input_prompt as ip
)

from ..models import (
    camper,
    inventory as inv,
    history
)
from .. import (
    var_const as vc,
    client
)

class CamperTransactions:
    purchase_time_format = "%a, %b %d, %Y | %I:%M:%S %p"
    
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
        self.master.option_add('*Dialog.msg.font', self.base_font)
        
        s = ttk.Style()
        s.theme_use('xpnative') # Default is "vista"
        s.configure('TNotebook.Tab', font=self.base_font)
        s.configure("TCombobox", darkcolor="grey", lightcolor="grey" )
        
        # ----- Declaring tk Variables
        self.gender = StringVar(value="Select Gender")
        self.camper_name = StringVar()
        self.last_purchase = StringVar( value="Month, day Year | 00:00:00 pm" )
        
        self.account_total = StringVar(value="${:,.2f}".format(0))
        self.sum_total = StringVar(value="${:,.2f}".format(0))
        self.donation = StringVar(value="${:,.2f}".format(0))
        self.returns = StringVar(value="${:,.2f}".format(0))
        self.remaining_balance = StringVar(value="${:,.2f}".format(0))
        
        self.cash = StringVar(value="${:,.2f}".format(0))
        
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
        
        self.active_camper = None
        
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
            width=15, textvariable=self.camper_name
        )
        # self.cmbo_name.set_completion_list(self.names)
        self.cmbo_name.bind('<<ComboboxSelected>>', self.populate_fields)
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
        
        # Last purchase labels.
        last_purchase_frame = Frame( self.header_frame )
        last_purchase_frame.pack(side=RIGHT, padx=5)
        Label(last_purchase_frame, text="Last Purchase", font=self.base_font).pack()
        self.lbl_last_purchase = Label(last_purchase_frame, textvariable=self.last_purchase, font=self.base_font)
        self.lbl_last_purchase.pack(padx=20)
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
        Label(self.footer_frame, text="Total In Account", font=self.base_font, anchor=S
            ).grid(row=0, column=0, padx=5)
        Label(self.footer_frame, textvariable=self.account_total, font=self.base_font, anchor=N
            ).grid(row=1, column=0, padx=5)

        Label(self.footer_frame, text="Total Item Price", font=self.base_font, anchor=S
            ).grid(row=0, column=1, padx=10, pady=10)
        Label(self.footer_frame, textvariable=self.sum_total, font=self.base_font, anchor=N
            ).grid(row=1, column=1, padx=5)

        Label(self.footer_frame, text="Donation", font=self.base_font, anchor=S
            ).grid(row=0, column=2, padx=5)
        Label(self.footer_frame, textvariable=self.donation, font=self.base_font, anchor=N
            ).grid(row=1, column=2, padx=5)

        Label(self.footer_frame, text="Returns", font=self.base_font, anchor=S
            ).grid(row=0, column=3, padx=5)
        Label(self.footer_frame, textvariable=self.returns, font=self.base_font, anchor=N
            ).grid(row=1, column=3, padx=5)

        Label(self.footer_frame, text="Remaining Balance", font=self.base_font, anchor=S
            ).grid(row=0, column=4, padx=5)
        self.lbl_rem_balance = Label(self.footer_frame, textvariable=self.remaining_balance, font=self.base_font, anchor=N
            )
        self.lbl_rem_balance.grid(row=1, column=4, padx=5)

        Label(self.footer_frame, text="Food Limit", font=self.base_font, anchor=S
            ).grid(row=0, column=5)
        self.lbl_food_limit = Label(self.footer_frame, textvariable=self.food_limit, font=self.base_font, anchor=N
            )
        self.lbl_food_limit.grid(row=1, column=5, padx=5)
        
        # Footer Right side
        Button(self.footer_frame, text="Cash", font=self.base_font,
            width=8, borderwidth=5, command=self.__cash
            ).grid(row=0, column=7, rowspan=2, padx=5, pady=1)
        
        Button(self.footer_frame, text="Donation", font=self.base_font,
            width=10, borderwidth=5, command=self.__donation
        ).grid(row=0, column=8, padx=5, pady=1)
        Button(self.footer_frame, text="Return", font=self.base_font,
            width=10, borderwidth=5, command=self.__returns
        ).grid(row=1, column=8, padx=5, pady=1)
        
        Button(self.footer_frame, text="Complete Transaction", font=self.base_font,
            width=20, borderwidth=5, command = self.complete_transaction
        ).grid(row=0, column=9, padx=5, pady=1)
        Button(self.footer_frame, text="Add Row", font=self.base_font, state="disabled",
            width=20, borderwidth=5, command=self.__add_row
        ).grid(row=1, column=9, padx=5, pady=1)
        
        # configure colume to seperate left and right
        Grid.columnconfigure(self.footer_frame, 6, weight=1)

    # ---------------------- Retrieving and displaying data
    # ----- Inventory Data
    def __load_inventory_names( self ):
        cmd = ("api/inventory/names", None)
        client.send( cmd )
        self.inventory_names = client.response_from_server()

    # ----- Camper Data
    def __update_cmbobox( self, e=None ):
        cmd = ("api/campers/names", self.gender.get().lower())
        client.send( cmd )
        self.camper_names = client.response_from_server()
        self.cmbo_name.config( value=self.camper_names )
    def populate_fields( self, e=None ):
        cmd = ("api/campers/camper", self.camper_name.get())
        client.send( cmd )
        self.active_camper = client.response_from_server()
        self.donation.set("${:,.2f}".format(0))
        self.returns.set("${:,.2f}".format(0))
        self.last_purchase.set( self.active_camper.last_purchase )
        self.account_total.set(
            "${:,.2f}".format(self.active_camper.curr_bal)
        )
        self.check_last_purchase()
    def update_values( self, e=None ):
        if self.camper_name.get() == "":
            messagebox.showerror("Error", "No camper selected.\nPlease select a camp and/or a camper.")
            return None
        total = 0
        food_limit = 0
        for row in self.rows:
            if row.data.col1["item"] is not None:
                if row.data.col1["item"].catagory == "Food & Drink":
                    food_limit += row.data.col1["item"].price * row.data.col1["spinbox_val"].get()
                total += row.data.col1["item"].price * row.data.col1["spinbox_val"].get()
            if row.data.col2["item"] is not None:
                if row.data.col2["item"].catagory == "Food & Drink":
                    food_limit += row.data.col2["item"].price * row.data.col2["spinbox_val"].get()
                total += row.data.col2["item"].price * row.data.col2["spinbox_val"].get()
            if row.data.col3["item"] is not None:
                if row.data.col3["item"].catagory == "Food & Drink":
                    food_limit += row.data.col3["item"].price * row.data.col3["spinbox_val"].get()
                total += row.data.col3["item"].price * row.data.col3["spinbox_val"].get()
            if row.data.col4["item"] is not None:
                if row.data.col4["item"].catagory == "Food & Drink":
                    food_limit += row.data.col4["item"].price * row.data.col4["spinbox_val"].get()
                total += row.data.col4["item"].price * row.data.col4["spinbox_val"].get()
            if row.data.col5["item"] is not None:
                if row.data.col5["item"].catagory == "Food & Drink":
                    food_limit += row.data.col5["item"].price * row.data.col5["spinbox_val"].get()
                total += row.data.col5["item"].price * row.data.col5["spinbox_val"].get()
        
        self.sum_total.set("${:,.2f}".format(total))
        self.remaining_balance.set(
            "${:,.2f}".format(
                float(self.account_total.get()[1:]) - 
                float(self.sum_total.get()[1:]) -
                float(self.donation.get()[1:]) -
                float(self.returns.get()[1:]) +
                float(self.cash.get()[1:])
            )
        )
        self.food_limit.set(
            "${:,.2f}".format(food_limit) + 
            "/${:,.2f}".format(vc.settings.food_limit)
        )
        limit_exceeded = self.check_food_limit()
        balance_exceeded = self.check_balance()
        if limit_exceeded:
            messagebox.showerror("Warning:", "Food Limit has been exceeded.")
        elif balance_exceeded[0]:
            if balance_exceeded[1]:
                messagebox.showerror("Error:", "Balance has fallen below 0.")
            else:
                messagebox.showwarning("Warning:",
                    """
                    Balance has reach 0.\n
                    Please confirm if this is desired.
                    """
                )
    def reset_content( self ):
        self.camper_name.set("")
        self.last_purchase.set("Month, day Year | 00:00:00 pm")
        
        self.account_total.set("${:,.2f}".format(0))
        self.sum_total.set("${:,.2f}".format(0))
        self.donation.set("${:,.2f}".format(0))
        self.returns.set("${:,.2f}".format(0))
        self.remaining_balance.set("${:,.2f}".format(0))
        
        self.cash.set("${:,.2f}".format(0))
        
        self.food_limit.set("${:,.2f}".format(0) + "/${:,.2f}".format(vc.settings.food_limit))
        
        self.active_camper = None
    def __cash( self ):
        ip.InputPrompt( title="Cash", return_data=self.cash, update=self.update_values )
    def __donation( self ):
        ip.InputPrompt( title="Donation", return_data=self.donation, update=self.update_values )
    def __returns( self ):
        ip.InputPrompt( title="Returns", return_data=self.returns, update=self.update_values )

    # ---------------------- Validation Checks & Complete Transaction.
    def check_last_purchase( self ):
        if self.last_purchase.get() != "00-00-00 00:00:00" or self.last_purchase.get() != "Month, day Year | 00:00:00 pm":
            now = datetime.now()
            lp = datetime.strptime( self.last_purchase.get(), self.__class__.purchase_time_format )
            delta = now - lp
            hours = divmod(delta.total_seconds(), 3600)
            if hours[0] < 2:
                self.lbl_last_purchase.config( fg="orange" )
                messagebox.showwarning("Warning", "Camper has made a purchase within the last 2 hours.")
            else:
                self.lbl_last_purchase.config( fg="black" )
    def check_food_limit( self ):
        food_total = self.food_limit.get().split("/")[0]
        if float(food_total[1:]) > vc.settings.food_limit:
            self.lbl_food_limit.config( fg="red" )
            return True
        else:
            self.lbl_food_limit.config( fg="black" )
            return False
    def check_balance( self ):
        if float(self.remaining_balance.get()[1:]) == 0:
            self.lbl_rem_balance.config( fg="orange" )
            return (True, False)
        elif float(self.remaining_balance.get()[1:]) < 0:
            self.lbl_rem_balance.config( fg="red" )
            return (True, True)
        else:
            self.lbl_rem_balance.config( fg="black" )
            return (False, None)
    def complete_transaction( self, e=None ):
        limit_exceeded = self.check_food_limit()
        balance_exceeded = self.check_balance()
        if limit_exceeded:
            messagebox.showerror("Error:", "Food Limit has been exceeded.")
        elif balance_exceeded[0]:
            if balance_exceeded[1]:
                messagebox.showerror("Error:", "Balance has fallen below 0.")
            else:
                messagebox.showwarning("Warning:",
                    """
                    Balance has reach 0.\n
                    Please confirm if this is desired.
                    """
                )
        else: # ---------- Complete Transaction.
            items = list()
            for row in self.rows:
                if row.data.col1["spinbox_val"].get() > 0 and row.data.col1["item"] is not None:
                    if row.data.col1["item"].catagory == "Clothing":
                        items.append(
                            (
                                f"{row.data.col1['listbox_val'].get()} | {row.data.col1['size_box_val'].get()}",
                                row.data.col1["spinbox_val"].get()
                            )
                        )
                    else:
                        items.append(
                            (
                                row.data.col1["listbox_val"].get(),
                                row.data.col1["spinbox_val"].get()
                            )
                        )
                if row.data.col2["spinbox_val"].get() > 0 and row.data.col2["item"] is not None:
                    if row.data.col2["item"].catagory == "Clothing":
                        items.append(
                            (
                                f"{row.data.col2['listbox_val'].get()} | {row.data.col2['size_box_val'].get()}",
                                row.data.col2["spinbox_val"].get()
                            )
                        )
                    else:
                        items.append(
                            (
                                row.data.col2["listbox_val"].get(),
                                row.data.col2["spinbox_val"].get()
                            )
                        )
                if row.data.col3["spinbox_val"].get() > 0 and row.data.col3["item"] is not None:
                    if row.data.col3["item"].catagory == "Clothing":
                        items.append(
                            (
                                f"{row.data.col3['listbox_val'].get()} | {row.data.col3['size_box_val'].get()}",
                                row.data.col3["spinbox_val"].get()
                            )
                        )
                    else:
                        items.append(
                            (
                                row.data.col3["listbox_val"].get(),
                                row.data.col3["spinbox_val"].get()
                            )
                        )
                if row.data.col4["spinbox_val"].get() > 0 and row.data.col4["item"] is not None:
                    if row.data.col4["item"].catagory == "Clothing":
                        items.append(
                            (
                                f"{row.data.col4['listbox_val'].get()} | {row.data.col4['size_box_val'].get()}",
                                row.data.col4["spinbox_val"].get()
                            )
                        )
                    else:
                        items.append(
                            (
                                row.data.col4["listbox_val"].get(),
                                row.data.col4["spinbox_val"].get()
                            )
                        )
                if row.data.col5["spinbox_val"].get() > 0 and row.data.col5["item"] is not None:
                    if row.data.col5["item"].catagory == "Clothing":
                        items.append(
                            (
                                f"{row.data.col5['listbox_val'].get()} | {row.data.col5['size_box_val'].get()}",
                                row.data.col5["spinbox_val"].get()
                            )
                        )
                    else:
                        items.append(
                            (
                                row.data.col5["listbox_val"].get(),
                                row.data.col5["spinbox_val"].get()
                            )
                        )
            
            now = datetime.now()
            purchase_info = {
                "date_time": now.strftime(self.__class__.purchase_time_format),
                "customer_name": self.camper_name.get(),
                "purchase_type": "Camper Account",
                "items": items,
                "sum_total": self.sum_total.get()
            }
            
            # ----- Updating Camper Account
            self.active_camper.curr_bal = float(self.remaining_balance.get()[1:])
            self.active_camper.curr_spent += float(self.sum_total.get()[1:])
            self.active_camper.total_donated += float(self.donation.get()[1:])
            self.active_camper.eow_return += float(self.donation.get()[1:])
            self.active_camper.last_purchase = now.strftime(self.__class__.purchase_time_format)
            
            # time.sleep(1)
            cmd = ("api/history/new_purchase", purchase_info)
            client.send( cmd )
            res = client.response_from_server()
            
            if res == client.SUCCESS_MSG:
                cmd = ("api/campers/update", self.active_camper)
                client.send( cmd )
                self.reset_content()
            else:
                messagebox.showerror("Error", res)
    

class Row:
    def __init__(self) -> None:
        self.col1 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar(),
            "size_box_val": StringVar(),
            "item": None
        }
        self.col2 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar(),
            "size_box_val": StringVar(),
            "item": None
        }
        self.col3 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar(),
            "size_box_val": StringVar(),
            "item": None
        }
        self.col4 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar(),
            "size_box_val": StringVar(),
            "item": None
        }
        self.col5 = {
            "spinbox_val": IntVar(),
            "listbox_val": StringVar(),
            "size_box_val": StringVar(),
            "item": None
        }