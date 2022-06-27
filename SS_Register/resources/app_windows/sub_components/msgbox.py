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
    Label( content_frame, text=content, font=base_font, bg="light grey", anchor=W ).pack( anchor=NW )
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
    Label( content_frame, text=content, font=base_font, bg="light grey", anchor=W ).pack( anchor=NW )
    btn = Button( content_frame, text="Dismiss", font=base_font, command=box.destroy, padx=20 )
    btn.pack( side=RIGHT, anchor=SE, pady=(20, 0) )
    btn.focus()
    
    __set_geometery( box )
    return box
