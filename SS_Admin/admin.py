from resources import server
import resources as r

from tkinter import mainloop
import threading

splash = None
"""
    Runs entire program.
    run using "py admin.py"
"""
def run():
    global splash
    splash = r.splash.Splash()
    
    server_thread = threading.Thread(target=server.start, args=())
    server_thread.daemon = True
    server_thread.start()
    
    splash.master.after(3000, main)
    mainloop()
    
    r.running = False

def main():
    global splash
    splash.master.destroy()
    
    r.main.MainDisplay()

if __name__ == '__main__':
    run()