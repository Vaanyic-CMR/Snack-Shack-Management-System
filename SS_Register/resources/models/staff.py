from .. import var_const as vc # import active_year
from datetime import datetime
import sqlite3 as sql

class Staff:
    db_name = f"databases/staff/{vc.active_year}_staff.db";
    tbl_name = "staff"
    
    def __init__( self, data ) -> None:
        self.id = data["rowid"]
        self.name = data["name"]
        self.pay_method = data["pay_method"]
        self.num_of_free_items = data["num_of_free_items"]
        self.last_free_item = data["last_free_item"]
        
        # Values of the account.
        self.init_bal = data["init_bal"]
        self.curr_bal = data["curr_bal"]
        self.curr_spent = data["curr_spent"]
        self.total_donated = data["total_donated"]
        self.eos_return = data["eos_return"]
        self.last_purchase = data["last_purchase"]
        
        self._created_at = data["created_at"]
        self._updated_at = data["updated_at"]
    
    """
        Instance Methods.
    """
    def created_at( self ):
        return self._created_at
    def updated_at( self ):
        return self._updated_at
    
    def to_dict( self ):
        data = {
            "id": self.id,
            "name": self.name,
            "pay_method": self.pay_method,
            "num_of_free_items": self.num_of_free_items,
            "last_free_item": self.last_free_item,
            
            "init_bal": self.init_bal,
            "curr_bal": self.curr_bal,
            "curr_spent": self.curr_spent,
            "total_donated": self.total_donated,
            "eos_return": self.eos_return,
            "last_purchase": self.last_purchase,
            
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
        return data
    
    def display( self ):
        print( ">>---------------<<" )
        print( "ID:", self.id )
        print( "Name:", self.name )
        print( "Pay Method:", self.pay_method )
        print( "Num Of Free Items:", self.num_of_free_items )
        print( "Last Free Item:", self.last_free_item )
        
        print( "Init Balance:", self.init_bal )
        print( "Current Balance:", self.curr_bal )
        print( "Total Donations:", self.total_donated )
        print( "End of Season Returns:", self.eos_return )
        print( "Last Purchase:", self.last_purchase )
        
        print( "Created At:", self._created_at )
        print( "Updated At:", self._updated_at )
        print( ">>---------------<<" )
    
    """
        Class Methods.
    """
    @classmethod
    def update_active_database( cls ):
        cls.db_name = f"databases/staff/{vc.active_year}_staff.db";
    @classmethod # Checks if the table exists within database. If not, creates one.
    def __table_check( cls ):
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute(f""" SELECT count(name) FROM sqlite_master
                WHERE type='table' AND name='{cls.db_name}' """)
        if c.fetchone()[0] != 1:
            c.execute( f"""CREATE TABLE {cls.tbl_name} (
                    name text,
                    pay_method text,
                    num_of_free_items integer,
                    last_free_item text,
                    
                    init_bal real,
                    curr_bal real,
                    curr_spent real,
                    total_donated real,
                    eos_return real,
                    last_purchase text,
                    
                    created_at text,
                    updated_at text )
                    """)
        conn.commit()
        conn.close()
    
    @classmethod
    def create( cls, data ):
        try:
            cls.__table_check()
        except:
            pass
            # print(e)
        
        now = datetime.now()
        data["created_at"] = now
        data["updated_at"] = now
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"""INSERT INTO {cls.tbl_name}
                VALUES (:name, :pay_method, :num_of_free_items, :last_free_item,
                :init_bal, :curr_bal, :curr_spent, :total_donated, :eos_return, :last_purchase,
                :created_at, :updated_at )""", data )
        conn.commit()
        conn.close()
    
    @classmethod
    def delete( cls, id ):
        try:
            cls.__table_check()
        except:
            pass
            # print(e)
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"DELETE FROM {cls.tbl_name} WHERE oid='{id}'" )
        conn.commit()
        conn.close()
    
    @classmethod
    def update( cls, data ):
        try:
            cls.__table_check()
        except:
            pass
            # print(e)
        
        data["updated_at"] = datetime.now()
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"""UPDATE {cls.tbl_name} SET
                name = :name,
                pay_method = :pay_method,
                num_of_free_items = :num_of_free_items,
                last_free_item = :last_free_item,
                
                init_bal = :init_bal,
                curr_bal = :curr_bal,
                curr_spent = :curr_spent,
                total_donated = :total_donated,
                eos_return = :eos_return,
                last_purchase = :last_purchase,
                
                updated_at = :updated_at
                
                WHERE oid = :id""", data)
        conn.commit()
        conn.close()
    
    @classmethod
    def get_all( cls ):
        try:
            cls.__table_check()
        except:
            pass
            # print(e)
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"SELECT oid, * FROM {cls.tbl_name}")
        query = [ dict(row) for row in c.fetchall() ]
        
        results = list()
        for q in query:
            results.append( cls(q) )
        
        conn.commit()
        conn.close()
        return results
    
    @classmethod
    def get_by_id( cls, id ):
        try:
            cls.__table_check()
        except:
            pass
            # print(e)
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name} WHERE oid={id}""")
        result = cls( dict( c.fetchall()[0] ) )
        
        conn.commit()
        conn.close()
        return result
    
    @classmethod
    def get_by_name( cls, name ):
        try:
            cls.__table_check()
        except:
            pass
            # print(e)
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE name='{name}'""")
        result = cls( dict( c.fetchall()[0] ) )
        
        conn.commit()
        conn.close()
        return result
    
    @classmethod
    def get_all_names( cls ):
        try:
            cls.__table_check()
        except:
            pass
            # print(e)
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        
        c.execute( f"""SELECT name FROM {cls.tbl_name}
                    ORDER BY name desc""")
        results = []
        
        for fetch in c.fetchall():
            results.append(fetch[0])
        
        conn.commit()
        conn.close()
        return results
    
    