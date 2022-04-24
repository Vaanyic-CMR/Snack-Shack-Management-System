from ..models import camper
from .. import var_const as vc

def handle_campers_command( data ):
    print( f"[COMMAND] Branch: 'campers' | {data}" )
    
    if data[0] == "api/campers/names":
        return camper.Camper.get_all_names_by_camp_and_gender(
            vc.active_camp, data[1]
        )

