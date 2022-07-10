from tkinter import *
from tkinter.font import Font
from PIL import ImageTk, Image

from ... import var_const as vc

# --------------------- Screen and Window Dimensions
def __set_geometery( box ):
    screen_width = box.winfo_screenwidth()
    screen_height = box.winfo_screenheight()
    
    window_width = box.winfo_width()
    window_height = box.winfo_height()
    
    window_position_x = int( screen_width/2 - window_width )
    window_position_y = int( screen_height/2 - window_height/2 )
    
    box.geometry( f"+{ window_position_x }+{ window_position_y }" )

# --------------------- Camper & Staff Info
def showcamper( camper ):
    box = Toplevel()
    box.title(f"SSMS | Camper Info")
    box.iconbitmap("resources/images/logo.ico")
    box.config( bg="light grey", relief="ridge", borderwidth=5, padx=10, pady=10 )
    box.transient()
    box.grab_set()
    
    title_font = Font(
        family = vc.settings.title_font["family"],
        size = vc.settings.title_font["size"]+5,
        weight = vc.settings.title_font["weight"]
    )
    base_font = Font(
        family = vc.settings.base_font["family"],
        size = vc.settings.base_font["size"]+3
    )
    
    Label( box, text=camper.name, font=title_font, bg="light grey", anchor=W ).pack( anchor=NW )
    
    Label( box, text=f"Initial Balance: {camper.init_bal}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    Label( box, text=f"Current Balance: {camper.curr_bal}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    Label( box, text=f"Current Spent: {camper.curr_spent}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    Label( box, text=f"Total Donated: {camper.total_donated}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    
    Label( box, text=f"End of Week Remainder: {camper.eow_remainder}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    
    btn = Button( box, text="Dismiss", font=base_font, command=box.destroy, padx=20 )
    btn.pack( side=RIGHT, anchor=SE, pady=(20, 0) )
    btn.focus()

def showstaff( staff ):
    box = Toplevel()
    box.title(f"SSMS | Staff Info")
    box.iconbitmap("resources/images/logo.ico")
    box.config( bg="light grey", relief="ridge", borderwidth=5, padx=10, pady=10 )
    box.transient()
    box.grab_set()
    
    title_font = Font(
        family = vc.settings.title_font["family"],
        size = vc.settings.title_font["size"]+5,
        weight = vc.settings.title_font["weight"]
    )
    base_font = Font(
        family = vc.settings.base_font["family"],
        size = vc.settings.base_font["size"]+3
    )
    
    Label( box, text=staff.name, font=title_font, bg="light grey", anchor=W ).pack( anchor=NW )
    
    Label( box, text=f"Initial Balance: {staff.init_bal}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    Label( box, text=f"Current Balance: {staff.curr_bal}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    Label( box, text=f"Current Spent: {staff.curr_spent}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    Label( box, text=f"Total Donated: {staff.total_donated}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    
    Label( box, text=f"# of Free Items: {staff.num_of_free_items}", font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    
    btn = Button( box, text="Dismiss", font=base_font, command=box.destroy, padx=20 )
    btn.pack( side=RIGHT, anchor=SE, pady=(20, 0) )
    btn.focus()

# --------------------- Error Box
def showerror( title, content, titlebar="Error" ):
    box = Toplevel()
    box.title(f"SSMS | {titlebar}")
    box.iconbitmap("resources/images/logo.ico")
    box.config( bg="light grey", relief="ridge", borderwidth=5 )
    box.transient()
    box.grab_set()
    
    title_font = Font(
        family = vc.settings.title_font["family"],
        size = vc.settings.title_font["size"]+5,
        weight = vc.settings.title_font["weight"]
    )
    base_font = Font(
        family = vc.settings.base_font["family"],
        size = vc.settings.base_font["size"]+3
    )
    
    img=ImageTk.PhotoImage(Image.open("resources/images/error.png"))
    Label( box, image=img#, relief="ridge"
        ).pack( side=LEFT, padx=10, pady=10 )
    
    # ----- Content Information
    content_frame = Frame( box, bg="light grey", padx=5, pady=5 )
    content_frame.pack( side=LEFT, fill=BOTH, expand=True, padx=5, pady=5 )
    
    Label( content_frame, text=title, font=title_font, fg="red", bg="light grey", anchor=W ).pack( anchor=NW )
    Label( content_frame, text=content, font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    btn = Button( content_frame, text="Dismiss", font=base_font, command=box.destroy, padx=20 )
    btn.pack( side=RIGHT, anchor=SE, pady=(20, 0) )
    btn.focus()
    
    __set_geometery( box )
    return box

def showwarning( title, content, titlebar="Warning" ):
    box = Toplevel()
    box.title(f"SSMS | {titlebar}")
    box.iconbitmap("resources/images/logo.ico")
    box.config( bg="light grey", relief="ridge", borderwidth=5 )
    box.transient()
    box.grab_set()
    
    title_font = Font(
        family = vc.settings.title_font["family"],
        size = vc.settings.title_font["size"]+5,
        weight = vc.settings.title_font["weight"]
    )
    base_font = Font(
        family = vc.settings.base_font["family"],
        size = vc.settings.base_font["size"]+3
    )
    
    img=ImageTk.PhotoImage(Image.open("resources/images/warning.png"))
    Label( box, image=img#, relief="ridge"
        ).pack( side=LEFT, padx=10, pady=10 )
    
    # ----- Content Information
    content_frame = Frame( box, bg="light grey", padx=5, pady=5 )
    content_frame.pack( side=LEFT, fill=BOTH, expand=True, padx=5, pady=5 )
    
    Label( content_frame, text=title, font=title_font, fg="orange", bg="light grey", anchor=W ).pack( anchor=NW )
    Label( content_frame, text=content, font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    btn = Button( content_frame, text="Dismiss", font=base_font, command=box.destroy, padx=20 )
    btn.pack( side=RIGHT, anchor=SE, pady=(20, 0) )
    btn.focus()
    
    __set_geometery( box )
    return box

def showinfo( title, content, titlebar="Info" ):
    box = Toplevel()
    box.title(f"SSMS | {titlebar}")
    box.iconbitmap("resources/images/logo.ico")
    box.config( bg="light grey", relief="ridge", borderwidth=5 )
    box.transient()
    box.grab_set()
    
    title_font = Font(
        family = vc.settings.title_font["family"],
        size = vc.settings.title_font["size"]+5,
        weight = vc.settings.title_font["weight"]
    )
    base_font = Font(
        family = vc.settings.base_font["family"],
        size = vc.settings.base_font["size"]+3
    )
    
    img=ImageTk.PhotoImage(Image.open("resources/images/info.png"))
    Label( box, image=img#, relief="ridge"
        ).pack( side=LEFT, padx=10, pady=10 )
    
    # ----- Content Information
    content_frame = Frame( box, bg="light grey", padx=5, pady=5 )
    content_frame.pack( side=LEFT, fill=BOTH, expand=True, padx=5, pady=5 )
    
    Label( content_frame, text=title, font=title_font, fg="orange", bg="light grey", anchor=W ).pack( anchor=NW )
    Label( content_frame, text=content, font=base_font, bg="light grey", anchor=W,
        wraplength=int(box.winfo_screenwidth()*0.4), justify=LEFT
    ).pack( anchor=NW )
    btn = Button( content_frame, text="Dismiss", font=base_font, command=box.destroy, padx=20 )
    btn.pack( side=RIGHT, anchor=SE, pady=(20, 0) )
    btn.focus()
    
    __set_geometery( box )
    return box