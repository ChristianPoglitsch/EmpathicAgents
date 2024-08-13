import socket
import sys
sys.path.append('../../')

from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.validation_dataclass import SystemMessage 
from LLM_Character.persona.persona import Persona
from LLM_Character.world.game import ReverieServer
# FIXME: what is the best way to get ahold of personas? how will this class interact with reverieserver? 
# ALSO THE SAME ISSUE FOR SIM_FOLDER, curr_time etc. 
# maybe this handler calls a function once again from reverieServer???
# OR dispatcher in reverieserver gives an instance of itself as argument. nah  

class UpdateDispatcher(BaseDispatcher):
    def handler(self, data:SystemMessage, server:ReverieServer):
        #     # TODO normally, you click on the unity character. so person_name should be provided in the byte_data message.
        #     # but we will hardcode it for now.
        #     # the same holds for information such as location.         
        #     # if it is a multi-character environment,
        #       then all names and all current location of those persona's should be sent as well. 

        # i think it is best to call some auxilary function from reverieservre to do this. 

        persona_name = "Camila" 
        curr_location = {
        "World" : "Reverie",
        "Sector" : "Kortrijk",
        "Arena" : "begijnehof"
        }
        server.
