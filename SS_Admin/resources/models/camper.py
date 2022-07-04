from .. import var_const as vc
from datetime import datetime
import sqlite3 as sql

class Camper:
    db_name = f"databases/campers/{vc.active_year}_campers.db";
    tbl_name = "campers"
    
    def __init__( self, data ) -> None:
        self.id = data["rowid"]
        
        # Camper data.
        self.name = data["name"]
        self.gender = data["gender"]
        self.camp = data["camp"]
        self.pay_method = data["pay_method"] # Cash, Check, Card, Scholarship, Multiple.
        
        # Values of the account
        self.init_bal = data["init_bal"]
        self.curr_bal = data["curr_bal"]
        self.curr_spent = data["curr_spent"]
        self.total_donated = data["total_donated"]
        self.eow_return = data["eow_return"]
        
        # Date of last purchase.
        self.last_purchase = data["last_purchase"]
        
        # What to do at end of week with the remainder.
        self.eow_remainder = data["eow_remainder"]
        
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
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "camp": self.camp,
            "pay_method": self.pay_method,
            "init_bal": self.init_bal,
            "curr_bal": self.curr_bal,
            "curr_spent": self.curr_spent,
            "total_donated": self.total_donated,
            "eow_return": self.eow_return,
            "last_purchase": self.last_purchase,
            "eow_remainder": self.eow_remainder,
            "created_at": self._created_at,
            "updated_at": self._updated_at }
    def to_string( self ):
        return (
            f"ID: {self.id}\n" +
            f"Name: {self.name}\n" +
            f"Gender: {self.gender}\n" +
            f"Camp: {self.camp}\n" +
            f"Payment Method: {self.pay_method}\n" +
            f"Initial Balance: {self.init_bal}\n" +
            f"Current Balance: {self.curr_bal}\n" +
            f"Current Spent: {self.curr_spent}\n" +
            f"Donations: {self.total_donated}\n" +
            f"Returns: {self.eow_return}\n" +
            f"Last Purchase: {self.last_purchase}\n" +
            f"EOW Remainder: {self.eow_remainder}\n" +
            f"Created At: {self._created_at}\n" +
            f"Updated At: {self._updated_at}\n" )
    
    def display( self ):
        print( ">>---------------<<" )
        print( "ID:", self.id )
        print( "Name:", self.name )
        print( "Gender:", self.gender )
        print( "Camp:", self.camp )
        print( "Payment Method:", self.pay_method )
        print( "Initial Balance:", self.init_bal )
        print( "Current Balance:", self.curr_bal )
        print( "Current Spent:", self.curr_spent )
        print( "Donations:", self.total_donated )
        print( "EOW Returns:", self.eow_return )
        print( "Last Purchase:", self.last_purchase )
        print( "EOW Remainder:", self.eow_remainder )
        print( "Created At:", self._created_at )
        print( "Updated At:", self._updated_at )
        print( ">>---------------<<" )
    
    """
        Class Methods.
    """
    @classmethod
    def update_active_database( cls ):
        cls.db_name = f"databases/campers/{vc.active_year}_campers.db";
    @classmethod # Checks if the table exists within database. If not, creates one.
    def __table_check( cls ):
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute(f""" SELECT count(name) FROM sqlite_master
                WHERE type='table' AND name='{cls.db_name}' """)
        if c.fetchone()[0] != 1:
            c.execute( f"""CREATE TABLE {cls.tbl_name} (
                    name text, gender text, camp text, pay_method text,
                    
                    init_bal real, curr_bal real, curr_spent real, total_donated real, eow_return real,
                    
                    last_purchase text,
                    
                    eow_remainder text,
                    
                    created_at text,
                    updated_at text )
                    """)
        conn.commit()
        conn.close()
    
    @classmethod
    def create( cls, data ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        now = datetime.now()
        data["created_at"] = now
        data["updated_at"] = now
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"""INSERT INTO {cls.tbl_name}
                VALUES (:name, :gender, :camp, :pay_method,
                :init_bal, :curr_bal, :curr_spent, :total_donated, :eow_return,
                :last_purchase, :eow_remainder, :created_at, :updated_at )""",
                data )
        conn.commit()
        conn.close()
    @classmethod
    def delete( cls, id ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"DELETE FROM {cls.tbl_name} WHERE oid={id}" )
        conn.commit()
        conn.close()
    @classmethod
    def update( cls, data ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        data["updated_at"] = datetime.now()
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        c.execute( f"""UPDATE {cls.tbl_name} SET
                name = :name,
                gender = :gender,
                camp = :camp,
                pay_method = :pay_method,
                init_bal = :init_bal,
                curr_bal = :curr_bal,
                curr_spent = :curr_spent,
                total_donated = :total_donated,
                eow_return = :eow_return,
                last_purchase = :last_purchase,
                eow_remainder = :eow_remainder,
                updated_at = :updated_at
                
                WHERE oid = :id""", data)
        conn.commit()
        conn.close()
    
    @classmethod
    def get_by_id( cls, id ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE oid={id}""")
        result = cls( dict( c.fetchone() ) )
        
        conn.commit()
        conn.close()
        return result
    @classmethod
    def get_by_name_and_camp( cls, name, camp ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE name='{name}' AND camp='{camp}'""")
        result = cls( dict( c.fetchall()[0] ) )
        
        conn.commit()
        conn.close()
        return result
    @classmethod
    def get_all( cls ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    ORDER BY name desc""")
        query = [ dict(row) for row in c.fetchall() ]
        
        results = list()
        for q in query:
            results.append( cls(q) )
        
        conn.commit()
        conn.close()
        return results
    
    @classmethod
    def get_all_names( cls ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        
        c.execute( f"""SELECT name FROM {cls.tbl_name}
                    ORDER BY name desc""")
        results = c.fetchall()
        
        conn.commit()
        conn.close()
        return results
    @classmethod
    def get_all_names_by_camp_and_gender( cls, camp, gender ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, name FROM {cls.tbl_name}
                    WHERE camp = '{camp}' AND gender = '{gender}'
                    ORDER BY name asc""")
        results = c.fetchall()
        
        data = list()
        for result in results:
            data.append(result[1])
        
        conn.commit()
        conn.close()
        return data
    @classmethod
    def get_all_names_by_camp( cls, camp ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        c = conn.cursor()
        
        c.execute( f"""SELECT name FROM {cls.tbl_name}
                    WHERE camp = '{camp}'
                    ORDER BY name desc""")
        results = []
        
        for fetch in c.fetchall():
            results.append(fetch[0])
        
        conn.commit()
        conn.close()
        return results
    
    @classmethod
    def get_all_by_camp( cls, camp ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE camp='{camp}'
                    ORDER BY gender desc, name asc""")
        query = [ dict(row) for row in c.fetchall() ]
        
        if len(query) == 0 and camp == "trailblazer":
            c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE camp='trail blazer'
                    ORDER BY gender desc, name asc""")
            query = [ dict(row) for row in c.fetchall() ]
        
        results = list()
        for q in query:
            results.append( cls(q) )
            if results[-1].camp == "trail blazer":
                results[-1].camp = "trailblazer"
                cls.update(results[-1].to_dict())
        
        conn.commit()
        conn.close()
        return results
    @classmethod
    def get_all_by_camp_sorted_by( cls, camp, sort ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE camp = '{camp}'
                    ORDER BY {sort} asc""")
        query = [ dict(row) for row in c.fetchall() ]
        
        results = list()
        for q in query:
            results.append( cls(q) )
        
        conn.commit()
        conn.close()
        return results
    @classmethod
    def get_all_sort_camp_gender_name( cls ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE camp = '{vc.active_camp}'
                    ORDER BY gender asc, name asc""")
        query = [ dict(row) for row in c.fetchall() ]
        
        results = list()
        for q in query:
            results.append( cls(q) )
        
        conn.commit()
        conn.close()
        return results
    
    @classmethod
    def get_all_by_camp_and_gender( cls, camp, gender ):
        try:
            cls.__table_check()
        except Exception as e:
            # print(e)
            pass
        
        conn = sql.connect( cls.db_name )
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        c.execute( f"""SELECT oid, * FROM {cls.tbl_name}
                    WHERE camp='{camp}' AND gender='{gender}'
                    ORDER BY name asc""")
        result = cls( dict( c.fetchall() ) )
        
        conn.commit()
        conn.close()
        return result
    
    