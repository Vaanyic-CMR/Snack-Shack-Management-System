from datetime import datetime
import json

class Settings:
    file_name = "resources/settings.json"
    
    def __init__( self, data ) -> None:
        self.host_name = data["host_name"]
        self.ports = data["ports"]
        self.station = data["station"]
        self.food_limit = data["food_limit"]
        self.dark_mode = data["dark_mode"]
        self.title_font = data["title_font"]
        self.base_font = data["base_font"]
    
    @staticmethod
    def to_dict( data ):
        data = {
            "host_name": data.host_name,
            "ports": data.ports,
            "station": data.station,
            "food_limit": data.food_limit,
            "dark_mode": data.dark_mode,
            "title_font": data.title_font,
            "base_font": data.base_font
        }
        return data
    
    @classmethod
    def load( cls ):
        data = json.load( open(cls.file_name) )
        return cls( data )
    
    @classmethod
    def save( cls, data ):
        settings = cls.to_dict( data )
        j = json.dumps( settings, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()