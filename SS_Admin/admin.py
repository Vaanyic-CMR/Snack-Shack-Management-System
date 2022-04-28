from resources import server
import resources as r

import threading

"""
    Runs entire program.
    run using "py admin.py"
"""

def main():
    app = r.main.MainDisplay()
    
    server_thread = threading.Thread(target=server.start, args=())
    server_thread.daemon = True
    server_thread.start()
    
    app.master.mainloop()
    
    r.running = False

if __name__ == '__main__':
    main()