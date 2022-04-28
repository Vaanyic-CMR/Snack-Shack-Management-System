from datetime import datetime
import json

from ..var_const import (
    datetime_format,
    active_year,
    active_camp)

class History:
    file_name = f"databases/purchase_history/{active_year}_{active_camp}.json"
    history_format = "%a, %b %d, %Y | %I:%M:%S %p"
    
    def __init__( self, data ) -> None:
        self.date_time = data["date_time"] # of format 'history_format'
        self.customer_name = data["customer_name"]
        self.purchase_type = data["purchase_type"]
        self.items = data["items"] # list of inventory items (name, quantity).
        self.sum_total = data["sum_total"]
        
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
        return {
            "date_time": self.date_time,
            "customer_name": self.customer_name,
            "purchase_type": self.purchase_type,
            "items": self.items,
            "sum_total": self.sum_total,
            
            "created_at": self._created_at.strftime(datetime_format),
            "updated_at": self._updated_at.strftime(datetime_format)
        }
    
    def display( self ):
        print( ">>---------------<<" )
        print( "Date/Time:", self.date_time )
        print( "Customer Name:", self.customer_name )
        print( "Purchase Type", self.purchase_type )
        print( "Items", self.items )
        print( "Sum Total", self.sum_total )
        print( "Created At:", self._created_at )
        print( "Updated At:", self._updated_at )
        print( ">>---------------<<" )
    
    """
        Class Methods.
    """
    @classmethod
    def update_active_database( cls ):
        cls.file_name = f"databases/purchase_history/{active_year}_{active_camp}.json"
    @classmethod
    def create_file( cls ):
        with open(cls.file_name, 'w+') as f:
            f.write('[]')
            f.close
    @classmethod
    def create( cls, data ):
        history = cls.get_all()
        
        now = datetime.now()
        data["created_at"] = now
        data["updated_at"] = now
        
        data["date_time"] = now.strftime(cls.history_format)
        history.append( cls(data) )
        
        # ----- Write to File
        results = list()
        for record in history:
            results.append( record.to_dict() )
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
    
    