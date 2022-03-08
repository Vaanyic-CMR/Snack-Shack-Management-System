from datetime import datetime
import sqlite3 as sql

class Bank:
    db_name = "databases/bank.db";
    tbl_name = "bank"
    
    def __init__( self, data ) -> None:
        # self.id = data["rowid"]
        self.year = data["year"]
        self.bank_total = data["bank_total"]
        
        self.cash_total = data["cash_total"]
        self.check_total = data["check_total"]
        self.card_total = data["card_total"]
        self.scholar_total = data["scholar_total"]
        
        self.camper_total = data["camper_total"]
        self.staff_total = data["staff_total"]
        
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
    @classmethod # Checks if the table exists within database. If not, creates one.
    def __table_check( cls ):
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute(f""" SELECT count(name) FROM sqlite_master
                WHERE type='table' AND name='{cls.db_name}' """)
        if c.fetchone()[0] != 1:
            c.execute( f"""CREATE TABLE {cls.tbl_name} (
                    year text,
                    bank_total real,
                    cash_total real,
                    check_total real,
                    card_total real,
                    scholar_total real,
                    camper_total real,
                    staff_total real,
                    
                    created_at text,
                    updated_at text ) """)
        conn.commit()
        conn.close()
    
    @classmethod
    def __year_check( cls, year ):
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        c.execute( f"""SELECT * FROM {cls.tbl_name} WHERE year={year}""")
        result = c.fetchall()
        conn.commit()
        conn.close()
        
        if len(result) > 0:
            return True
        else:
            return False
    
    @classmethod
    def __update( cls, data ):
        try:
            cls.__table_check()
        except:
            print(f"Table '{cls.tbl_name}' Exists")
        
        data["updated_at"] = datetime.now()
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"""UPDATE {cls.tbl_name} SET
                bank_total = :bank_total,
                cash_total = :cash_total,
                check_total = :check_total,
                card_total = :card_total,
                scholar_total = :scholar_total,
                camper_total = :camper_total,
                staff_total = :staff_total,
                
                updated_at = :updated_at
                
                WHERE year = :year""", data)
        conn.commit()
        conn.close()
    
    @classmethod
    def save( cls, data ):
        try:
            cls.__table_check()
        except:
            print(f"Table '{cls.tbl_name}' Exists")
        
        if cls.__year_check( data["year"] ):
            cls.__update( data )
        else:
            now = datetime.now()
            data["created_at"] = now
            data["updated_at"] = now
            
            conn = sql.connect( cls.db_name )
            c = conn.cursor()
            c.execute( f"""INSERT INTO {cls.tbl_name}
                    VALUES (:year, :bank_total,
                    :cash_total, :check_total, :card_total, :scholar_total,
                    :camper_total, :staff_total,
                    :created_at, :updated_at )""", data )
            conn.commit()
            conn.close()
    
    @classmethod
    def delete( cls, year ):
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"DELETE FROM {cls.tbl_name} WHERE year='{year}'" )
        conn.commit()
        conn.close()
    
    @classmethod
    def get_all( cls ):
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
    def get_by_year( cls, year ):
        try:
            cls.__table_check()
        except:
            print(f"Table '{cls.tbl_name}' Exists")
        
        if cls.__year_check( year ):
            conn = sql.connect( cls.db_name )
            conn.row_factory = sql.Row
            c = conn.cursor()
            
            c.execute( f"""SELECT * FROM {cls.tbl_name} WHERE year={year}""")
            result = c.fetchall()
            
            conn.commit()
            conn.close()
            return cls(dict( result[0] ))
        else:
            now = datetime.now()
            
            data = {
                "year": year,
                "bank_total": 0.0,
                
                "cash_total": 0.0,
                "check_total": 0.0,
                "card_total": 0.0,
                "scholar_total": 0.0,
                
                "camper_total": 0.0,
                "staff_total": 0.0,
                
                "created_at": now,
                "updated_at": now
            }
            cls.save( data )
            return cls( data )
    