from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.communication.incoming_messages import UpdateMessage 
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication.udp_comms import UdpComms

class UpdateDispatcher(BaseDispatcher):
    def handler(self, socket:UdpComms, serverM:ReverieServerManager, model:LLM_API, data:UpdateMessage):
        client_id = socket.udpIP + socket.udpSendPort
        server = serverM.getServer(client_id)
        if server and server.isloaded(client_id): 
            server.update_processor(data.data)
            # TODO update also user possession. 
            # NOTE send confirmation back to unity that everything went fine?
            # socket.sendData(...)
        else :
            # FIXME: have proper error messages. 
            socket.SendData("Error: Select a saved game first or start a new game.") 
