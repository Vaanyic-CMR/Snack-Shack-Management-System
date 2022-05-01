from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font

from datetime import datetime
from turtle import pu

from . import (
    settings as sett_window,
    staff_transactions,
    camper_transactions
)
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

class CashTransactions:
    purchase_time_format = "%a, %b %d, %Y | %I:%M:%S %p"
    
    def __init__(self) -> None:
        # --------------------- Title Bar and General
        self.master = Tk()
        self.master.title("Snack Shack Management System | Cash Register")
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
        self.name = StringVar()
        
        self.sum_total = StringVar(value="${:,.2f}".format(0))
        self.cash_received = StringVar(value="${:,.2f}".format(0))
        self.donation = StringVar(value="${:,.2f}".format(0))
        self.change = StringVar(value="${:,.2f}".format(0))
        
        # ----- Initializing Frames
        self.header_frame = Frame( self.master, relief="ridge", borderwidth=5 )
        self.header_frame.pack( fill=X )
        self.body_frame = Frame( self.master )
        self.body_frame.pack( fill=BOTH, expand=True, pady=10 )
        self.footer_frame = Frame( self.master, relief="ridge", borderwidth=5 )
        self.footer_frame.pack( fill=X )#.place( relwidth=1, relx=0.5, rely=1, anchor=S )
        
        # ----- Variables
        self.rows = list()
        self.inventory_names = list()
        
        # ----- Constructing main builds
        self.__menu_bar()
        self.__build_header()
        self.__build_body()
        self.__build_footer()
        
        # Add a row of transaction items.
        self.__add_row()
        
        self.__set_geometery()
    
    # --------------------- Open Other Windows
    def __open_camper( self ):
        self.master.destroy()
        camper_transactions.CamperTransactions()
    def __open_staff( self ):
        self.master.destroy()
        staff_transactions.StaffTransactions()
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

        # Options Menu
        self.option_menu = Menu(self.t_menu, tearoff=False)
        self.t_menu.add_cascade(label='Options', menu=self.option_menu)
        self.option_menu.add_command(label='Settings', command=lambda : sett_window.Settings(self, "cash"))
        self.option_menu.add_command(label='About')#, command=self.openAbout)
    def _on_mousewheel(self, event):
        self.body_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    # ---------------------- Contruct Components
    def __build_header( self ):
        Label(self.header_frame, text = "Cash Transactions", font = self.title_font
            ).pack(side=LEFT, padx=15, pady=5)
        
        self.name_entry = Entry( self.header_frame, font=self.base_font, width=15,
            textvariable=self.name
        )
        self.name_entry.pack(side=LEFT, padx=5, pady=5)
        self.name_entry.focus()
        
        # Staff Button
        Button(self.header_frame, text="Staff", width=10, borderwidth=5,
            font=self.base_font, command=self.__open_staff
        ).pack(side=RIGHT, padx=5, pady=5)
        # Camper Button
        Button(self.header_frame, text="Camper", width=10, borderwidth=5,
            font=self.base_font, command=self.__open_camper
        ).pack(side=RIGHT, padx=5, pady=5)
    def __build_body( self ):
        self.body_canvas = Canvas( self.body_frame )
        self.body_canvas.pack( side=LEFT, fill=BOTH, expand=True )
        body_scrollbar = ttk.Scrollbar( self.body_frame , orient=VERTICAL, command=self.body_canvas.yview )
        body_scrollbar.pack( side=RIGHT, fill=Y )
        
        # Configure Canvas
        self.body_canvas.configure( yscrollcommand=body_scrollbar.set )
        self.body_canvas.bind( '<Configure>',
            lambda e: self.body_canvas.configure(scrollregion=self.body_canvas.bbox("all")) )
        self.body_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
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
        Label(self.footer_frame, text="Sum Total", font=self.base_font, anchor=S
            ).grid(row=0, column=0, padx=10, pady=10)
        Label(self.footer_frame, textvariable=self.sum_total, font=self.base_font, anchor=N
            ).grid(row=1, column=0, padx=5)
        
        Label(self.footer_frame, text="Cash Received", font=self.base_font, anchor=S
            ).grid(row=0, column=1, padx=5)
        Label(self.footer_frame, textvariable=self.cash_received, font=self.base_font, anchor=N
            ).grid(row=1, column=1, padx=5)
        
        Label(self.footer_frame, text="Donation", font=self.base_font, anchor=S
            ).grid(row=0, column=2, padx=5)
        Label(self.footer_frame, textvariable=self.donation, font=self.base_font, anchor=N
            ).grid(row=1, column=2, padx=5)
        
        Label(self.footer_frame, text="Change Due", font=self.base_font, anchor=S
            ).grid(row=0, column=3, padx=10, pady=10)
        self.lbl_change = Label(self.footer_frame, textvariable=self.change, font=self.base_font, anchor=N
            )
        self.lbl_change.grid(row=1, column=3, padx=5)
        
        # Footer Right side
        Button(self.footer_frame, text="Donation", font=self.base_font,
            width=10, borderwidth=5, command=self.__donation
        ).grid(row=1, column=5, padx=10, pady=1)
        Button(self.footer_frame, text="Cash", font=self.base_font,
            width=10, borderwidth=5, command=self.__cash
            ).grid(row=0, column=5, padx=10, pady=1)
        
        Button(self.footer_frame, text="Complete Transaction", font=self.base_font,
            width=20, borderwidth=5, command = self.complete_transaction
        ).grid(row=0, column=6, padx=10, pady=1)
        Button(self.footer_frame, text="Add Row", font=self.base_font, state="disabled",
            width=20, borderwidth=5, command=self.__add_row
        ).grid(row=1, column=6, padx=10, pady=1)
        
        # configure colume to seperate left and right
        Grid.columnconfigure(self.footer_frame, 4, weight=1)

    # ---------------------- Retrieving and displaying data
    # ----- Inventory Data
    def __load_inventory_names( self ):
        cmd = ("api/inventory/names", None)
        client.send( cmd )
        self.inventory_names = client.response_from_server()

    def update_values( self, e=None ):
        total = 0
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
        change = float(self.cash_received.get()[1:]) - total
        self.change.set("${:,.2f}".format(change))
        self.__check_change()
    def reset_content( self ):
        self.name.set("")
        
        self.sum_total.set("${:,.2f}".format(0))
        self.cash_received.set("${:,.2f}".format(0))
        self.donation.set("${:,.2f}".format(0))
        self.change.set("${:,.2f}".format(0))
        
        for row in self.rows:
            row.reset_widgets()
    def __donation( self ):
        ip.InputPrompt( title="Donation", return_data=self.donation, update=self.update_values )
    def __cash( self ):
        ip.InputPrompt( title="Cash Received", return_data=self.cash_received, update=self.update_values )

    # ---------------------- Validation Checks & Complete Transaction.
    def __check_change( self ):
        if float(self.change.get()[1:]) < 0:
            self.lbl_change.config( fg="orange" )
            return False
        else:
            self.lbl_change.config( fg="black" )
            return True
    def complete_transaction( self, e=None ):
        if not self.__check_change():
            messagebox.showerror("Error", "Change is Negative\nMore cash from customer is required.")
            return None
        
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
        
        if len(items) <= 0:
            messagebox.showerror("Error", """No list of items.\nMake sure selected items have a quantity.""")
            return None
        
        now = datetime.now()
        purchase_info = {
            "date_time": now.strftime(self.__class__.purchase_time_format),
            "customer_name": "",
            "purchase_type": "",
            "items": items,
            "sum_total": self.sum_total.get()
        }
        if self.name.get() == "":
            purchase_info["customer_name"] = "Unknown"
        else:
            purchase_info["customer_name"] = self.name.get()
        
        purchase_types = list()
        if float(self.cash_received.get()[1:]) > 0:
            purchase_types.append("Cash")
        if float(self.donation.get()[1:]) > 0:
            purchase_types.append("Donation")
        
        for idx, pt in enumerate(purchase_types):
            if idx == 0:
                purchase_info["purchase_type"] += pt
            else:
                purchase_info["purchase_type"] += f" | {pt}"
        
        cmd = ("api/history/new_purchase", purchase_info)
        client.send( cmd )
        res = client.response_from_server()
        
        if float(self.cash_received.get()[1:]) > 0 and res == client.SUCCESS_MSG:
            cmd = ("api/bank/cash", float(self.cash_received.get()[1:]))
            client.send( cmd )
            res = client.response_from_server()
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
