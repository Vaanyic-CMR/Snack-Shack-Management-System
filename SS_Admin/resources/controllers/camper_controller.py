from ..models import camper
from .. import var_const as vc

def handle_campers_command( data ):
    print( f"[COMMAND] Branch: 'campers' | {data}" )
    
    if data[0] == "api/campers/names":
        return camper.Camper.get_all_names_by_camp_and_gender(
            vc.active_camp, data[1]
        )
    if data[0] == "api/campers/camper":
        return camper.Camper.get_by_name_and_camp(
            name=data[1], camp=vc.active_camp
        )
    if data[0] == "api/campers/update":
        return camper.Camper.update( data[1].to_dict() )
    