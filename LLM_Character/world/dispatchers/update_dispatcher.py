import socket
import sys
sys.path.append('../../')

from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.validation_dataclass import UpdateMessage 
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication_module.udp_comms import UdpComms

class UpdateDispatcher(BaseDispatcher):
    def handler(self, socket:UdpComms, server:ReverieServer, model:LLM_API, data:UpdateMessage):
        server.update_processor(data.data)
        # TODO update also user possession. 

        #NOTE send confirmation back to unity that everything went fine?
        # socket.sendData(...)
