from datetime import datetime
import json

from ..var_const import datetime_format

class Inventory:
    file_name = "databases/inventory.json"
    
    def __init__( self, data ) -> None:
        self.name = data["name"]
        self.catagory = data["catagory"]
        self.in_stock = data["in_stock"]
        self.price = data["price"]
        self.threshold = data["threshold"]
        
        self.sizes = list()
        if data["sizes"] != None:
            for s in data["sizes"]:
                self.sizes.append( Size(s) )
        
        self._created_at = data["created_at"]
        self._updated_at = data["updated_at"]
    
    """
        Instance Methods.
    """
    def created_at( self ):
        return self.created_at
    def updated_at( self ):
        return self._updated_at
    
    def to_dict( self ):
        dict_sizes = list()
        for s in self.sizes:
            dict_sizes.append( s.to_dict() )
        
        return {
            "name": self.name,
            "catagory": self.catagory,
            "in_stock": self.in_stock,
            "price": self.price,
            "threshold": self.threshold,
            
            "sizes": dict_sizes,
            
            "created_at": self._created_at.strftime(datetime_format),
            "updated_at": self._updated_at.strftime(datetime_format)
        }
    
    def display( self ):
        print( ">>---------------<<" )
        print( "Name:", self.name )
        print( "Catagory:", self.catagory )
        print( "In Stock", self.in_stock )
        print( "Price", self.price )
        print( "Threshold", self.threshold )
        for size in self.sizes:
            size.display()
        print( "Created At:", self._created_at )
        print( "Updated At:", self._updated_at )
        print( ">>---------------<<" )
    
    def get_size( self, size ):
        for s in self.sizes:
            if s.size == size:
                return s
        return False
    
    """
        Class Methods.
    """
    @classmethod # Pass in a dictionary.
    def create( cls, data ):
        inv = cls.get_all()
        
        now = datetime.now()
        data["created_at"] = now
        data["updated_at"] = now
        
        if len(inv) == 0 or data["name"] > inv[-1].name:
            inv.append( cls(data) )
        elif data["name"] < inv[0].name:
            inv.insert( 0, cls(data) )
        elif len(inv) > 1:
            n = 0;
            while n < ( len(inv) - 1 ):
                if data["name"] > inv[n].name and data["name"] < inv[n+1].name:
                    inv.insert( n+1, cls(data) )
                    n+=1
                n+=1
        else:
            print("Error: could not find location to save Inventory Data.")
        
        # ----- Write to File
        results = list()
        for i in inv:
            results.append( i.to_dict() )
        j = json.dumps( results, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    @classmethod
    def delete( cls, name ):
        results = json.load( open(cls.file_name) )
        for result in results:
            if result["name"] == name:
                results.remove(result)
        
        j = json.dumps( results, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    @classmethod
    def update( cls, data ):
        now = datetime.now().strftime(datetime_format)
        data["updated_at"] = now
        
        results = json.load( open(cls.file_name) )
        for index, result in enumerate(results):
            if result["name"] == data["name"]:
                results[index] = data
        
        j = json.dumps( results, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    
    @classmethod
    def get_all( cls ):
        results = json.load( open(cls.file_name) )
        data = list()
        for result in results:
            result["created_at"] = datetime.strptime( result["created_at"], datetime_format )
            result["updated_at"] = datetime.strptime( result["updated_at"], datetime_format )
            data.append( cls(result) )
        return data
    @classmethod
    def get_by_name( cls, name ):
        results = json.load( open(cls.file_name) )
        for result in results:
            if result["name"] == name:
                result["created_at"] = datetime.strptime( result["created_at"], datetime_format )
                result["updated_at"] = datetime.strptime( result["updated_at"], datetime_format )
                return cls( result )
        return None
    @classmethod
    def get_all_names( cls ):
        results = json.load( open(cls.file_name) )
        data = list()
        for result in results:
            data.append( result["name"] )
        return data
    
    @classmethod # Probably not nessesary.
    def add_size( cls, data ):
        pass

class Size:
    def __init__( self, data ) -> None:
        self.size = data["size"]
        self.in_stock = data["in_stock"]
        self.threshold = data["threshold"]
    
    """
        Instance Methods.
    """
    def to_dict( self ):
        return {
            "size": self.size,
            "in_stock": self.in_stock,
            "threshold": self.threshold
        }
    
    def display( self ):
        print( ">>-------" )
        print( "Size:", self.size )
        print( "In Stock:", self.in_stock )
        print( "Threshold:", self.threshold )
        print( ">>-------" )
    