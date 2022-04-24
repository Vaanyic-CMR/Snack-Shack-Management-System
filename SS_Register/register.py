from resources import client
import resources as r

"""
    Runs entire program.
    run using "py admin.py"
"""
def main():
    app = r.main.Main()
    app.master.mainloop()
    
    # r.running = False
    
    client.send( client.DISCONNECT_CMD )

if __name__ == '__main__':
    main()