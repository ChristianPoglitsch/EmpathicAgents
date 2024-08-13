import json
import sys
sys.path.append('../../')

from LLM_Character.world.validation_dataclass import PromptMessage
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.persona.persona import Persona
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_api import LLM_API
from LLM_Character.udp_comms import UdpComms

class PromptDispatcher(BaseDispatcher) : 
  def handler(self, socket:UdpComms, server:ReverieServer, model:LLM_API, data: PromptMessage):
    # TODO normally, you click on the unity character. so person_name should be provided in the byte_data message.
    # FIXME: sender must also be known, at least the persona constructed around him, which is needed in conversing i think ? maybe not, after all its a single player sim.  
    persona_message = data.data.message
    persona_name = data.data.persona_name
    response = server.prompt_processor(persona_name, persona_message, model)
    data.data.value = data.data.value + 1
    data.data.message = response 
    obj = data.model_dump_json()
    socket.SendData(obj)
