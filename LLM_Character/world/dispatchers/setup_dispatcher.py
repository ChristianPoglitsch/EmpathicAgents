import socket
import sys
sys.path.append('../../')

from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.validation_dataclass import SetupMessage 
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication_module.udp_comms import UdpComms

class SetupDispatcher(BaseDispatcher):
    def handler(sself, socket:UdpComms, server:ReverieServer, model:LLM_API, data:SetupMessage):
        server.loads(data.data)

        #NOTE send confirmation back to unity that everything went fine?
        # socket.sendData(...)