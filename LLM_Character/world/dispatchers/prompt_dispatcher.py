import json

from LLM_Character.world.validation_dataclass import PromptMessage
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication_module.udp_comms import UdpComms

class PromptDispatcher(BaseDispatcher) : 
  def handler(self, socket:UdpComms, server:ReverieServer, model:LLM_API, data: PromptMessage):       
    if server.isloaded():
      pd = data.data 
      utt, emotion, trust = server.prompt_processor(pd.user_name,  pd.persona_name, pd.message, model)
      sending_data = {
        "message" : utt,
        "emotion" : emotion,
        "trust" : trust,
      }
      sending_str = json.dumps(sending_data) 
      socket.SendData(sending_str)

