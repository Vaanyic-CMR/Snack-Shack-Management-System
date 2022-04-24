from ..models import inventory as inv
from .. import var_const as vc

def handle_inventory_command( data ):
    print( f"[COMMAND] Branch: 'inventory' | {data}" )
    
    if data[0] == "api/inventory/names":
        return inv.Inventory.get_all_names()



