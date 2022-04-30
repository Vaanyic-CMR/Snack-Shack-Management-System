from resources import client
import resources as r

from tkinter import mainloop

splash = None
"""
    Runs entire program.
    run using "py admin.py"
"""
def run():
    global splash
    splash = r.splash.Splash()
    
    splash.master.after(3000, main)
    mainloop()
    
    client.send( client.DISCONNECT_CMD )

def main():
    global splash
    splash.master.destroy()
    
    r.main.Main()

if __name__ == '__main__':
    run()