from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.communication.incoming_messages import StartMessage
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication.udp_comms import UdpComms

class StartDispatcher(BaseDispatcher):
    def handler(sself, socket:UdpComms, serverM:ReverieServerManager, model:LLM_API, data:StartMessage):
        clientid = socket.udpIP + str(socket.udpSendPort) 
        
        sd = data.data
        if serverM.get_server(clientid):
            print("error, client alreasy exists??")
            return None 

        server = ReverieServer(sd.fork_sim_code, sd.sim_code, clientid)
        serverM.add_connection(clientid, server)
        server.start_processor()
        print("Done")
        socket.SendData("Done")
        #NOTE send confirmation back to unity that everything went fine?
        # socket.sendData(...)