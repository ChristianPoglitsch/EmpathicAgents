import json

from LLM_Character.communication.incoming_messages import PromptMessage
from LLM_Character.communication.outgoing_messages import PromptReponseMessage, PromptResponseData
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication.udp_comms import UdpComms

class PromptDispatcher(BaseDispatcher) : 
  def handler(self, socket:UdpComms, serverM:ReverieServerManager, model:LLM_API, data: PromptMessage):       
    # FIXME: ibrahim: obviously the client-id should be automatically extracted from the connection
    client_id = socket.udpIP + str(socket.udpSendPort)
    server = serverM.get_server(client_id)
    if server and server.is_loaded():
      pd = data.data 
      utt, emotion, trust = server.prompt_processor(pd.user_name,  pd.persona_name, pd.message, model)
      response_data = PromptResponseData(utt=utt, emotion=emotion, trust_level=str(trust))
      response_message = PromptReponseMessage(type="PromptReponseMessage", data=response_data)
      sending_str = response_message.model_dump_json()
      print("Done")
      socket.SendData(sending_str)
    else:
      print("Error: Select a saved game first or start a new game.")
      # FIXME: have proper error messages. 
      socket.SendData("Error: Select a saved game first or start a new game.") 