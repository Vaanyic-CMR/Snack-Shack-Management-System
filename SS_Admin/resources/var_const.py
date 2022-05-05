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
    settings = s.Settings({
        "host_name": socket.gethostname(),
        "port": 9000,
        "food_limit": 2.0,
        "dark_mode": False,
        "title_font": {
            "family": "monospace",
            "size": 16,
            "weight": "bold"
        },
        "base_font": {
            "family": "monospace",
            "size": 10
        },
        "table_header_font": {
            "family": "monospace",
            "size": 13,
            "weight": "bold"
        },
        "table_row_font": {
            "family": "monospace",
            "size": 11
        }
    })
    s.Settings.save(settings.to_dict())
def reload_settings():
    global settings
    settings = s.Settings.load()

# ---------- Variables
running = True

active_camp = "select camp"
def change_active_camp( camp ):
    global active_camp
    active_camp = camp
    pass

active_year = now.strftime("%Y")
def change_active_year( year ):
    global active_year
    active_year = year
    pass

datetime_format = "%Y-%m-%d %H:%M:%S.%f"

# ---------- constants
