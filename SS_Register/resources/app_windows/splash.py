from tkinter import *

from PIL import ImageTk, Image

# from resources import var_const as vc

class Splash:
    def __init__( self ) -> None:
        self.master = Tk()
        self.master.title("SSMS - Splash")
        self.image = ImageTk.PhotoImage( Image.open( "resources/images/splash.jpg") )
        Label( self.master, image=self.image ).pack()
        
        # -------------- Position Screen on Center
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        x = int( (screen_width / 2) - ( 518 / 2) )
        y = int( (screen_height / 2) - ( 192 / 2) )
        
        self.master.geometry( f"518x192+{x}+{y}" )
        
        self.master.overrideredirect( True )
    
    def close( self ):
        self.master.destroy()