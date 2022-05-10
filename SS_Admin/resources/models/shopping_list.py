from datetime import datetime
import json

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
        return {
            "name": self.name,
            "in_stock": self.in_stock,
            "threshold": self.threshold,
            "time_on_list": self.time_on_list
        }
    
    """
        Class Methods.
    """
    @classmethod
    def create_file( cls ):
        j = json.dumps( [], indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    @classmethod
    def get_all( cls ):
        results =  cls.__load()
        cls.__save(results)
        return results
    
    @classmethod
    def __load( cls ):
        results = json.load( open(cls.file_name) )
        data = list()
        for result in results:
            data.append( cls(result) )
        return data
    @classmethod
    def __save( cls, data ):
        results = list()
        for d in data:
            results.append( d.to_dict() )
        
        j = json.dumps( results, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    @classmethod
    def update( cls, item ):
        data = cls.__load()
        for index, d in enumerate(data):
            if d.name == item["name"]:
                data[index].in_stock = item["in_stock"]
                data[index].threshold = item["threshold"]
        cls.__save(data)
    @classmethod
    def delete( cls, item ):
        data = cls.__load()
        
        new_list=list()
        for index, d in enumerate(data):
            if d.name != item["name"]:
                new_list.append( d )
        cls.__save( new_list )
    
    @classmethod
    def add_item( cls, item, catagory=None ):
        sl = cls.__load()
        new_item = None
        if catagory == "Clothing":
            new_item = cls({
                "name": f"{item['name']} | {item['size']}",
                "in_stock": item['in_stock'],
                "threshold": item['threshold'],
                "time_on_list": [
                    datetime.now().strftime(cls.date_format),
                    "0 Days"
                ]
            })
        else:
            new_item = cls({
                "name": item['name'],
                "in_stock": item["in_stock"],
                "threshold": item["threshold"],
                "time_on_list": [
                    datetime.now().strftime(cls.date_format),
                    "0 Days"
                ]
            })
        sl.append(new_item)
        cls.__save( sl )
    @classmethod
    def In( cls, item ):
        results = cls.__load()
        for result in results:
            if item == result.name:
                return True
        return False
    
    