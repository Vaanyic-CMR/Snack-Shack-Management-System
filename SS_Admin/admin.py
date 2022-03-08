import resources as r

from datetime import datetime
import threading as thd

"""
    Runs entire program.
    run using "py admin.py"
"""
def splash():
    s = r.splash.Splash()
    print("Splash Active.")
    s.master.after(5000, s.close())
    # s.master.mainloop()
    print("Splash Inactive.")

def main():
    app = r.main.MainDisplay()
    app.master.mainloop()
    
    # print(r.running)
    # print(r.active_year)

if __name__ == '__main__':
    main()