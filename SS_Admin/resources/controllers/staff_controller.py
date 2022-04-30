from ..models import staff
from .. import var_const as vc

def handle_staff_command( data ):
    print( f"[COMMAND] Branch: 'staff' | {data}" )
    
    if data[0] == "api/staff/names":
        return staff.Staff.get_all_names()
    if data[0] == "api/staff/staffer":
        return staff.Staff.get_by_name(name=data[1])
    if data[0] == "api/staff/update":
        return staff.Staff.update( data[1].to_dict() )