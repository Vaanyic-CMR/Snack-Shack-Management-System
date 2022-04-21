from ast import operator
from datetime import datetime
import json
from turtle import update

from . import inventory as inv_m

class Shopping_List:
    file_name = "databases/shopping_list.json";
    date_format = "%m/%d/%Y"
    
    def __init__( self, data ) -> None:
        self.name = data["name"]
        self.in_stock = data["in_stock"]
        self.threshold = data["threshold"]
        
        then = datetime.strptime( data["time_on_list"][0], self.__class__.date_format )
        now = datetime.now()
        delta = now - then
        self.time_on_list = [ data["time_on_list"][0], f"{delta.days} Days" ]
    
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
    def get_all( cls ):
        # cls.update_list()
        results =  cls.load()
        cls.save(results)
        return results
    
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
    def update( cls, item ):
        data = cls.load()
        for index, d in data:
            if d.name == item.name:
                data[index].in_stock = item.in_stock
                data[index].threshold = item.threshold
        cls.save(data)
    
    @classmethod
    def delete( cls, item ):
        data = cls.load()
        
        for index, d in data:
            if d.name == item.name:
                del data[index]
        cls.save( data )
    
    @classmethod
    def add_item( cls, inv_data ):
        sl = cls.load()
        new_item = cls({
            "name": inv_data.name,
            "in_stock": inv_data.in_stock,
            "threshold": inv_data.threshold,
            "time_on_list": [
                datetime.now().strftime(cls.date_format),
                "0 Days"
            ]
        })
        new_sl = sl.append(new_item)
        cls.save( new_sl )
    
    @classmethod
    def __in( cls, item ):
        results = cls.load()
        for result in results:
            if item.name == result.name:
                return True
        return False
    
    
    
    