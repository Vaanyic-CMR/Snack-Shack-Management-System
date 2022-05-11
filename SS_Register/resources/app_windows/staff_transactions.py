from datetime import datetime
import time

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font

from . import (
    settings as sett_window,
    camper_transactions,
    cash_transactions
)
from .sub_components import (
    transaction_row as tr,
    input_prompt as ip
)
from ..models import (
    staff,
    inventory as inv,
    history
)
from .. import (
    var_const as vc,
    client
)

class StaffTransactions:
    purchase_time_format = "%a, %b %d, %Y | %I:%M:%S %p"
    
    def __init__(self) -> None:
        # --------------------- Title Bar and General
        self.master = Tk()
        self.master.title("Snack Shack Management System | Staff Register")
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
        self.staff_name = StringVar()
        self.free_item_name = StringVar(value="Select Free Item")
        self.last_free_item = StringVar( value="Month, day Year | 00:00:00 pm" )
        
        self.account_total = StringVar(value="${:,.2f}".format(0))
        self.sum_total = StringVar(value="${:,.2f}".format(0))
        self.donation = StringVar(value="${:,.2f}".format(0))
        self.returns = StringVar(value="${:,.2f}".format(0))
        self.remaining_balance = StringVar(value="${:,.2f}".format(0))
        
        self.cash = StringVar(value="${:,.2f}".format(0))
        
        # ----- Initializing Frames
        self.header_frame = Frame( self.master, relief="ridge", borderwidth=5 )
        self.header_frame.pack( fill=X )
        self.body_frame = Frame( self.master )
        self.body_frame.pack( fill=BOTH, expand=True, pady=10 )
        self.footer_frame = Frame( self.master, relief="ridge", borderwidth=5 )
        self.footer_frame.pack( fill=X )
        
        # ----- Variables
        self.rows = list()
        self.staff_names = list()
        self.inventory_names = list()
        self.food_drink_names = list()
        self.__load_food_drink_names()
        
        self.free_item = None
        self.active_staffer = None
        
        # ----- Constructing main builds
        self.__menu_bar()
        self.__build_header()
        self.__build_body()
        self.__build_footer()
        
        # Pulling Data from server.
        self.__update_cmbobox()
        
        # Add a row of transaction items.
        self.__add_row()
        
        self.__set_geometery()
    
    # --------------------- Open Other Windows
    def __open_cash( self ):
        self.master.destroy()
        cash_transactions.CashTransactions()
    def __open_camper( self ):
        self.master.destroy()
        camper_transactions.CamperTransactions()
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
        self.file_menu.add_command(label='Reset Content', command=self.reset_content)
        self.file_menu.add_command(label='Reload Staff Names', command=self.__update_cmbobox)

        # Options Menu
        self.option_menu = Menu(self.t_menu, tearoff=False)
        self.t_menu.add_cascade(label='Options', menu=self.option_menu)
        self.option_menu.add_command(label='Settings', command=lambda : sett_window.Settings(self, "staff"))
        self.option_menu.add_command(label='About')#, command=self.openAbout)
    def __on_mousewheel(self, event):
        self.body_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    # ---------------------- Contruct Components
    def __build_header( self ):
        Label(self.header_frame, text="Staff Transactions", font=self.title_font
            ).pack(side=LEFT, padx=15, pady=5)
        
        self.cmbo_name = ttk.Combobox( self.header_frame, font=self.base_font,
            width=15, textvariable=self.staff_name
        )
        # self.cmbo_name.set_completion_list(self.names)
        self.cmbo_name.bind('<<ComboboxSelected>>', self.populate_fields)
        self.cmbo_name.pack(side=LEFT, padx=5, pady=5)
        self.cmbo_name.focus()
        
        # Cash Button
        self.btnCash = Button(self.header_frame, text="Cash", width=10,
                            borderwidth=5, font=self.base_font, command=self.__open_cash)
        self.btnCash.pack(side=RIGHT, padx=5, pady=5)
        # Staff Button
        self.btnStaff = Button(self.header_frame, text="Campers", width=10,
                            borderwidth=5, font=self.base_font, command=self.__open_camper)
        self.btnStaff.pack(side=RIGHT, padx=5, pady=5)
        
        # Last purchase labels & Free Item OptionMenu.
        last_free_item_frame = Frame( self.header_frame )
        last_free_item_frame.pack(side=RIGHT, padx=5)
        Label(last_free_item_frame, text="Last Free Item", font=self.base_font).grid(row=0, column=1)
        self.lbl_last_free_item = Label(last_free_item_frame, textvariable=self.last_free_item, font=self.base_font)
        self.lbl_last_free_item.grid(row=1, column=1)
        
        free_item_menu = OptionMenu( last_free_item_frame, self.free_item_name, *self.food_drink_names, command=self.__get_free_item )
        free_item_menu.config( font=self.base_font )
        self.master.nametowidget(free_item_menu.menuname).config( font=self.base_font )
        free_item_menu.grid(row=0, column=0, rowspan=2, padx=10)
    def __build_body( self ):
        self.body_canvas = Canvas( self.body_frame )
        self.body_canvas.pack( side=LEFT, fill=BOTH, expand=True )
        body_scrollbar = ttk.Scrollbar( self.body_frame , orient=VERTICAL, command=self.body_canvas.yview )
        body_scrollbar.pack( side=RIGHT, fill=Y )
        
        # Configure Canvas
        self.body_canvas.configure( yscrollcommand=body_scrollbar.set )
        self.body_canvas.bind( '<Configure>',
            lambda e: self.body_canvas.configure(scrollregion=self.body_canvas.bbox("all")) )
        # self.body_canvas.bind_all("<MouseWheel>", self.__on_mousewheel)
        
        # New canvas frame
        self.canvas_frame = Frame( self.body_canvas )
        self.body_canvas.create_window((0,0), window=self.canvas_frame, anchor=NW )
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
        
        # Footer Right side
        Button(self.footer_frame, text="Cash\n(With Account)", font=self.base_font,
            width=15, borderwidth=5, command=self.__cash
            ).grid(row=0, column=6, rowspan=2, padx=5, pady=1)
        
        Button(self.footer_frame, text="Donation", font=self.base_font,
            width=10, borderwidth=5, command=self.__donation
        ).grid(row=0, column=7, padx=5, pady=1)
        Button(self.footer_frame, text="Return", font=self.base_font,
            width=10, borderwidth=5, command=self.__returns
        ).grid(row=1, column=7, padx=5, pady=1)
        
        Button(self.footer_frame, text="Complete Transaction", font=self.base_font,
            width=20, borderwidth=5, command = self.complete_transaction
        ).grid(row=0, column=8, padx=5, pady=1)
        Button(self.footer_frame, text="Add Row", font=self.base_font, state="disabled",
            width=20, borderwidth=5, command=self.__add_row
        ).grid(row=1, column=8, padx=5, pady=1)
        
        # configure colume to seperate left and right
        Grid.columnconfigure(self.footer_frame, 5, weight=1)

    # ---------------------- Retrieving and displaying data
    # ----- Inventory Data
    def __load_inventory_names( self ):
        cmd = ("api/inventory/names", None)
        client.send( cmd )
        self.inventory_names = client.response_from_server()
    def __load_food_drink_names( self ):
        cmd = ("api/inventory/food_drink", None)
        client.send( cmd )
        self.food_drink_names = client.response_from_server()
    def __get_free_item( self, e=None ):
        if self.free_item_name.get() != "Select Free Item":
            cmd = ("api/inventory/item", self.free_item_name.get())
            client.send( cmd )
            self.free_item = client.response_from_server()

    # ----- Staff Data
    def __update_cmbobox( self, e=None ):
        cmd = ("api/staff/names", None)
        client.send( cmd )
        self.staff_names = client.response_from_server()
        self.cmbo_name.config( value=self.staff_names )
    def populate_fields( self, e=None ):
        cmd = ("api/staff/staffer", self.staff_name.get())
        client.send( cmd )
        self.active_staffer = client.response_from_server()
        self.last_free_item.set( self.active_staffer.last_free_item )
        self.account_total.set("${:,.2f}".format(self.active_staffer.curr_bal))
        self.donation.set("${:,.2f}".format(0))
        self.returns.set("${:,.2f}".format(0))
        self.remaining_balance.set(self.account_total.get())
        self.check_last_free_item()
    def update_values( self, e=None ):
        if self.staff_name.get() == "":
            messagebox.showerror("Error", "No staffer selected.\nPlease select a staff member.")
            return None
        total = 0.0
        for row in self.rows:
            if row.data.col1["item"] is not None:
                total += row.data.col1["item"].price * row.data.col1["spinbox_val"].get()
            if row.data.col2["item"] is not None:
                total += row.data.col2["item"].price * row.data.col2["spinbox_val"].get()
            if row.data.col3["item"] is not None:
                total += row.data.col3["item"].price * row.data.col3["spinbox_val"].get()
            if row.data.col4["item"] is not None:
                total += row.data.col4["item"].price * row.data.col4["spinbox_val"].get()
            if row.data.col5["item"] is not None:
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
        balance_exceeded = self.check_balance()
        if balance_exceeded[0]:
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
        self.staff_name.set("")
        self.free_item_name.set("Select Free Item")
        self.last_free_item.set("Month, day Year | 00:00:00 pm")
        
        self.account_total.set("${:,.2f}".format(0))
        self.sum_total.set("${:,.2f}".format(0))
        self.donation.set("${:,.2f}".format(0))
        self.returns.set("${:,.2f}".format(0))
        self.remaining_balance.set("${:,.2f}".format(0))
        
        self.cash.set("${:,.2f}".format(0))
        
        self.free_item = None
        self.active_staffer = None
        
        for row in self.rows:
            row.reset_widgets()
    def __cash( self ):
        ip.InputPrompt( title="Cash", return_data=self.cash, update=self.update_values )
    def __donation( self ):
        ip.InputPrompt( title="Donation", return_data=self.donation, update=self.update_values )
    def __returns( self ):
        ip.InputPrompt( title="Returns", return_data=self.returns, update=self.update_values )

    # ---------------------- Validation Checks & Complete Transaction.
    def check_last_free_item( self ):
        if self.last_free_item.get() != "00-00-00 00:00:00" and self.last_free_item.get() != "Month, day Year | 00:00:00 pm":
            now = datetime.now()
            lp = datetime.strptime( self.last_free_item.get(), self.__class__.purchase_time_format )
            delta = now - lp
            hours = divmod(delta.total_seconds(), 3600)
            if hours[0] < 12:
                self.lbl_last_free_item.config( fg="orange" )
                messagebox.showwarning("Warning", "staff member has recieved a free item within the last 12 hours.")
            else:
                self.lbl_last_purchase.config( fg="black" )
    def check_balance( self ):
        if float(self.remaining_balance.get()[1:]) == 0 and float(self.cash.get()[1:]) <= 0:
            self.lbl_rem_balance.config( fg="orange" )
            return (True, False)
        elif float(self.remaining_balance.get()[1:]) < 0:
            self.lbl_rem_balance.config( fg="red" )
            return (True, True)
        else:
            self.lbl_rem_balance.config( fg="black" )
            return (False, None)
    def complete_transaction( self, e=None ):
        balance_exceeded = self.check_balance()
        if balance_exceeded[0]:
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
            if self.free_item != None:
                items.append((self.free_item_name.get(), 1))
            
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
            
            if len(items) <= 0:
                messagebox.showerror("Error", """No list of items.\nMake sure selected items have a quantity.""")
                return None
            
            now = datetime.now()
            purchase_info = {
                "date_time": now.strftime(self.__class__.purchase_time_format),
                "customer_name": self.staff_name.get(),
                "purchase_type": "",
                "items": items,
                "sum_total": self.sum_total.get()
            }
            purchase_types = list()
            if self.free_item_name.get() != "Select Free Item":
                purchase_types.append("Free Item")
            if float(self.remaining_balance.get()[1:]) != self.active_staffer.curr_bal and float(self.sum_total.get()[1:]) > 0:
                purchase_types.append("Account")
            if float(self.donation.get()[1:]) > 0:
                purchase_types.append("Donation")
                items.append( ( "Donation", self.donation.get() ) )
            if float(self.returns.get()[1:]) > 0:
                purchase_types.append("Returns")
                items.append( ( "Return", self.returns.get() ) )
            if float(self.cash.get()[1:]) > 0 and float(self.sum_total.get()[1:]) > 0:
                purchase_types.append("Cash")
            
            for idx, pt in enumerate(purchase_types):
                if idx == 0:
                    purchase_info["purchase_type"] += pt
                else:
                    purchase_info["purchase_type"] += f" | {pt}"
            
            # ----- Updating Camper Account
            if self.account_total.get() != self.remaining_balance.get():
                self.active_staffer.curr_spent += float(self.sum_total.get()[1:]) - float(self.cash.get()[1:])
            self.active_staffer.curr_bal = float(self.remaining_balance.get()[1:])
            self.active_staffer.total_donated += float(self.donation.get()[1:])
            self.active_staffer.eos_return += float(self.returns.get()[1:])
            if self.free_item_name.get() != "Select Free Item": # Check if staff member is getting a free item.
                self.active_staffer.num_of_free_items += 1
                self.active_staffer.last_free_item = now.strftime(self.__class__.purchase_time_format)
            if float(self.sum_total.get()[1:]) > 0:
                self.active_staffer.last_purchase = now.strftime(self.__class__.purchase_time_format)
            
            cmd = ("api/history/new_purchase", purchase_info)
            client.send( cmd )
            res = client.response_from_server()
            
            if float(self.cash.get()[1:]) > 0 and res == client.SUCCESS_MSG:
                cmd = ("api/bank/cash", float(self.cash.get()[1:]))
                client.send( cmd )
                res = client.response_from_server()
            if float(self.donation.get()[1:]) > 0 and res == client.SUCCESS_MSG:
                cmd = ("api/bank/donation", float(self.donation.get()[1:]))
                client.send( cmd )
                res = client.response_from_server()
            
            if res == client.SUCCESS_MSG:
                cmd = ("api/staff/update", self.active_staffer)
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