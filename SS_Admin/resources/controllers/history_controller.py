from ..models import (
    history,
    inventory as inv
)
from .. import var_const as vc
from .. import server

def handle_history_command( data ):
    print( f"[COMMAND] Branch: 'history' | {data}" )
    
    if data[0] == "api/history/new_purchase":
        updated_items = list()
        for index, item in enumerate(data[1]["items"]):
            
            name = item[0].split("|")
            i = inv.Inventory.get_by_name( name[0].strip() )
            
            if i.catagory == "Clothing":
                for idx, size in enumerate(i.sizes):
                    if size.size == name[1].strip():
                        if i.sizes[idx].in_stock - item[1] >= 0:
                            i.sizes[idx].in_stock -= item[1]
                        else:
                            return f"Not enough inventory for {item[1]} of {item[0]}"
            else:
                if i.in_stock - item[1] >= 0:
                    i.in_stock -= item[1]
                else:
                    return f"Not enough inventory for {item[1]} of {item[0]}"
            updated_items.append(i.to_dict())
        
        for updated_item in updated_items:
            inv.Inventory.update(updated_item)
        history.History.create( data[1] )
        return server.SUCCESS_MSG
    
    