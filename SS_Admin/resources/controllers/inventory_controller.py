from ..models import inventory as inv
from .. import (
    var_const as vc,
    server
)

def handle_inventory_command( data ):
    print( f"[COMMAND] Branch: 'inventory' | {data}" )
    
    if data[0] == "api/inventory/names":
        return inv.Inventory.get_all_names()
    if data[0] == "api/inventory/cloth_names":
        return inv.Inventory.get_all_clothing_names()
    if data[0] == "api/inventory/food_drink":
        return inv.Inventory.get_all_food_drink_names()
    if data[0] == "api/inventory/item":
        return inv.Inventory.get_by_name( data[1] )
    # return server.FAIL_MSG
