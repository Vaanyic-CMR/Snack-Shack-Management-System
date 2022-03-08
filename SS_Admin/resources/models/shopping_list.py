from datetime import datetime
import json

class Shopping_List:
    file_name = "databases/shopping_list.json";
    
    def __init__( self, data ) -> None:
        self.name = data["name"]
        self.in_stock = data["in_stock"]
        self.threshold = data["threshold"]
        self.time_on_list = data["time_on_list"]
    
    """
        Instance Methods.
    """
    def display( self ):
        print( ">>---------------<<" )
        print( "Name:", self.name )
        print( "In Stock", self.in_stock )
        print( "Threshold", self.threshold )
        print( "Time on List:", self.time_on_list )
        print( ">>---------------<<" )
    
    def to_dict( self ):
        data = {
            "name": self.name,
            "in_stock": self.in_stock,
            "threshold": self.threshold,
            "time_on_list": self.time_on_list
        }
        return data
    
    """
        Class Methods.
    """
    @classmethod
    def load( cls ):
        results = json.load( open(cls.file_name) )
        data = list()
        for result in results:
            data.append( cls(result) )
        return data
    
    @classmethod
    def save( cls, data ):
        results = list()
        for d in data:
            results.append( d.to_dict() )
        
        j = json.dumps( results, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    
    @classmethod
    def delete( cls, data, item ):
        for d in data:
            if d.name == item:
                del d
        cls.save( data )
    
    @classmethod
    def update( cls ):
        pass