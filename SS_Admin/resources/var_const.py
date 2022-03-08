"""
    Storage location for any unrelated app variables or app wide constants.
"""
from .models import settings as s
from datetime import datetime
import socket

now = datetime.now()

# ---------- Settings
try:
    settings = s.Settings.load()
except Exception as e:
    print( e )
    settings = {
        "host_name": socket.gethostname(),
        "ports": [ 3330, 3331 ],
        "station": "boys",
        "food_limit": 2.0,
        "dark_mode": False,
        "title_font": {
            "family": "monospace",
            "size": 16,
            "weight": "bold"
        },
        "base_font": {
            "family": "monospace",
            "size": 13
        }
    }

# ---------- Variables
running = True
active_year = now.strftime("%Y")
datetime_format = "%Y-%m-%d %H:%M:%S.%f"

# ---------- constants
