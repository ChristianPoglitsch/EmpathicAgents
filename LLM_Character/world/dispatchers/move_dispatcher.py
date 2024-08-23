from LLM_Character.communication.outgoing_messages import MoveResponse, MoveResponseData
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.communication.incoming_messages import MetaData, MoveMessage  
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication.udp_comms import UdpComms

class MoveDispatcher(BaseDispatcher):
    def handler(self, socket:UdpComms, serverM:ReverieServerManager, model:LLM_API, data:MoveMessage):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded(): 
            movements = server.move_processor(data.data, model)
            
            move_response_data = MoveResponseData(**movements)
            move_response = MoveResponse(type="movement", data=move_response_data)
            move_str = move_response.model_dump_json() 
            print("Done") 
            socket.SendData(move_str)
        else :
            # FIXME: have proper error messages. 
            socket.SendData("Error: Select a saved game first or start a new game.") 


