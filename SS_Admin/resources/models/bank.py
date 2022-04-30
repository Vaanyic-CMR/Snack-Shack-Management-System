from datetime import datetime
import json

from .. import var_const as vc # import vc.active_year, vc.datetime_format
from . import camper, staff

class Bank:
    file_name = "databases/bank.json"
    
    def __init__( self, data ):
        self.year = data["year"]
        self.bank_total = data["bank_total"]
        
        self.cash_total = data["cash_total"]
        self.check_total = data["check_total"]
        self.card_total = data["card_total"]
        self.scholar_total = data["scholar_total"]
        
        self.camper_total = data["camper_total"]
        self.staff_total = data["staff_total"]
        
        self._created_at = datetime.strptime( data["created_at"], vc.datetime_format )
        self._updated_at = datetime.strptime( data["updated_at"], vc.datetime_format )
    
    """
        Instance Methods.
    """
    def created_at( self ):
        return self.created_at
    def updated_at( self ):
        return self._updated_at
    
    def to_dict( self ):
        data = {
            "year": self.year,
            "bank_total": self.bank_total,
            "cash_total": self.cash_total,
            "check_total": self.check_total,
            "card_total": self.card_total,
            "scholar_total": self.scholar_total,
            "camper_total": self.camper_total,
            "staff_total": self.staff_total,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
        return data
    
    def display( self ):
        print( ">>---------------<<" )
        print( "Year:", self.year )
        print( "Bank Total:", self.bank_total )
        print( "Cash Total:", self.cash_total )
        print( "Check Total:", self.check_total )
        print( "Card Total:", self.card_total)
        print( "Scholarship Total:", self.scholar_total )
        print( "Camper Total:", self.camper_total )
        print( "Staff Total:", self.staff_total )
        print( "Created At:", self._created_at )
        print( "Updated At:", self._updated_at )
        print( ">>---------------<<" )
    
    """
        Class Methods.
    """
    @classmethod
    def __create( cls, data ):
        bnk = cls.get_all( JSON=True )
        
        now = datetime.now()
        data["created_at"] = now.strftime(vc.datetime_format)
        data["updated_at"] = now.strftime(vc.datetime_format)
        
        bnk.append( data )
        
        # ----- Write to File
        j = json.dumps( bnk, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    @classmethod
    def __update( cls, data ):
        now = datetime.now().strftime(vc.datetime_format)
        data["updated_at"] = now
        
        results = json.load( open(cls.file_name) )
        for index, result in enumerate(results):
            if result["year"] == data["year"]:
                data["created_at"] = result["created_at"]
                results[index] = data
        
        j = json.dumps( results, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    @classmethod
    def save( cls, data ):
        year_exists = False
        bnk = cls.get_all( JSON=True )
        
        for b in bnk:
            if b["year"] == data["year"]:
                year_exists = True
                break
        
        if year_exists:
            cls.__update( data )
        else:
            cls.__create( data )
    @classmethod
    def delete( cls, year ):
        results = json.load( open(cls.file_name) )
        for result in results:
            if result["year"] == year:
                results.remove(result)
        
        j = json.dumps( results, indent = 4 )
        with open(cls.file_name, 'w') as f:
            f.write(j)
            f.close()
    @classmethod
    def update_fields( cls ):
        campers = camper.Camper.get_all()
        staff_members = staff.Staff.get_all()
        bank = {
            "year": vc.active_year,
            "bank_total": 0,
            
            "cash_total": 0,
            "check_total": 0,
            "card_total": 0,
            "scholar_total": 0,
            
            "camper_total": 0,
            "staff_total": 0
        }
        
        for c in campers:
            bank["bank_total"] += c.init_bal
            bank["bank_total"] -= c.eow_return
            bank["camper_total"] += c.init_bal
            bank["camper_total"] -= c.eow_return
            if c.pay_method == "cash":
                bank["cash_total"] += c.init_bal
            elif c.pay_method == "check":
                bank["check_total"] += c.init_bal
            elif c.pay_method == "card":
                bank["card_total"] += c.init_bal
            elif c.pay_method == "scholarship":
                bank["scholar_total"] += c.init_bal
        
        for s in staff_members:
            bank["bank_total"] += s.init_bal
            bank["bank_total"] -= s.eos_return
            bank["staff_total"] += s.init_bal
            bank["staff_total"] -= s.eos_return
            if s.pay_method == "cash":
                bank["cash_total"] += s.init_bal
            elif s.pay_method == "check":
                bank["check_total"] += s.init_bal
            elif s.pay_method == "card":
                bank["card_total"] += s.init_bal
            elif s.pay_method == "scholarship":
                bank["scholar_total"] += s.init_bal
        
        cls.save( bank )
    
    @classmethod
    def get_all( cls, JSON=False ):
        results = json.load( open(cls.file_name) )
        if not JSON:
            data = list()
            for result in results:
                data.append( cls(result) )
            return data
        return results
    @classmethod
    def get_all_years( cls ):
        results = json.load( open(cls.file_name) )
        data = list()
        for result in results:
            data.append( result["year"] )
        return data
    @classmethod
    def get_by_year( cls, year ):
        results = json.load( open(cls.file_name) )
        for result in results:
            if result["year"] == year:
                return cls( result )
        return None
    
    