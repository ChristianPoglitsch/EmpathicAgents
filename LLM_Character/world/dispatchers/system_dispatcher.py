import socket
import sys
sys.path.append('../../')

from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.validation_dataclass import SetupMessage 
from LLM_Character.persona.persona import Persona
from LLM_Character.world.game import ReverieServer
# FIXME: what is the best way to get ahold of personas? how will this class interact with reverieserver? 
# ALSO THE SAME ISSUE FOR SIM_FOLDER, curr_time etc. 
# maybe this handler calls a function once again from reverieServer???
# OR dispatcher in reverieserver gives an instance of itself as argument. nah  

class SetupDispatcher(BaseDispatcher):
    def handler(self, data:SetupMessage, server:ReverieServer):
        server.loads(data.data)
