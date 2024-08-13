import datetime
import sys
sys.path.append('../../')

from LLM_Character.world.validation_dataclass import PromptMessage
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.persona.persona import Persona
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_api import LLM_API
from LLM_Character.udp_comms import UdpComms

# FIXME: what is the best way to get ahold of personas? how will this class interact with reverieserver? 
class PromptDispatcher(BaseDispatcher) : 
  def handler(self, socket:UdpComms, server:ReverieServer, model:LLM_API, data: PromptMessage):
    # TODO normally, you click on the unity character. so person_name should be provided in the byte_data message.
    # but we will hardcode it for now.
    # example: persona_name = data.data.persona_name
    persona_message = data.data.message
    persona_name = data.data.persona_name
    persona_name = "Camila"
    server.prompt_processor(persona_name)

    # send response back if needed.
    socket.SendData("nice") 
    self.step += 1
    self.curr_time += datetime.timedelta(seconds=self.sec_per_step)

