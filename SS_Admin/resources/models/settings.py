from datetime import datetime
import json

class Settings:
    file_name = "resources/settings.json"
    
    def __init__( self, data ) -> None:
        self.host_name = data["host_name"]
        self.port = data["port"]
        self.food_limit = data["food_limit"]
        self.dark_mode = data["dark_mode"]
        self.title_font = data["title_font"]
        self.base_font = data["base_font"]
        self.table_header_font = data["table_header_font"]
        self.table_row_font = data["table_row_font"]
    
    def to_dict( self ):
        data = {
            "host_name": self.host_name,
            "port": self.port,
            "food_limit": self.food_limit,
            "dark_mode": self.dark_mode,
            "title_font": self.title_font,
            "base_font": self.base_font,
            "table_header_font": self.table_header_font,
            "table_row_font": self.table_row_font
        }
        return data
    
    @classmethod
    def load( cls ):
        data = json.load( open(cls.file_name) )
        return cls( data )
    @classmethod
    def save( cls, data ):
        j = json.dumps( data, indent=4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()