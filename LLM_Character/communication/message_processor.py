import json 
from typing import Type, Union

from LLM_Character.communication.incoming_messages import BaseMessage
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher
from LLM_Character.world.dispatchers.setup_dispatcher import SetupDispatcher
from LLM_Character.world.dispatchers.update_dispatcher import UpdateDispatcher 
from LLM_Character.communication.incoming_messages import PromptMessage, SystemMessage, UpdateMessage
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication.udp_comms import UdpComms

# ------------------------
# FIXME: HOE ZORG JE ERVOOR DAT HET STATELESS MAAR DAT JE EERST SETUP MESSAGE UITVOERT EN DAN PAS MOVEMESSAGE OF PROMPTMESSAGE???
# of 
# IK DENK DAT IK EEN SERVER MANAGER OF IETS IN DIE SOORT NODIG ZAL HEBBEN. 
# want stel twee requests binnen met (verschillende of zelfde) sim_code ??? dan hebben we ook een probleem
# we moeten bijhouden wat er precies mogelijk is en wat niet.
# en de servermanager, is een dict van connection/socket -> reverieserver ? 
# ------------------------ 

# NOTE: ibrahim: temporary class which will be replaced by the hungarian team? 
# after all, they are going to use grpc, and so most of the socket programmming will dissapear
# no need to make it complicated for now, (assume single client single server), but the server (revererieserver) takes in client-id
# which makes it possible to run multiple instances for different clients without having a conflict. 
class MessageProcessor:
    def __init__(self):
        self._dispatch_map: dict[str, BaseDispatcher] = {}
        self._validator_map: dict[str, Type[BaseMessage]] = {}

        self.register('PromptMessage', PromptMessage, PromptDispatcher())
        self.register('SetupData', SystemMessage, SetupDispatcher())
        self.register('UpdateData', UpdateMessage, UpdateDispatcher())

    def register(self, message_type: str, message_class:Type[BaseMessage], dispatcher_class:BaseDispatcher):
        self._validator_map[message_type] = message_class
        self._dispatch_map[message_type] = dispatcher_class 
    
    def dispatch(self, socket: UdpComms, server:ReverieServer, model: LLM_API, data:BaseMessage):
      
      self._dispatch_map[data.type].handler(socket, server, model, data)

    def validate_data(self, data: str) -> Union[BaseMessage,None]:
        try:
            loaded_data = json.loads(data)
            data_type = loaded_data.get('type')
            schema = self._validator_map.get(data_type)
            if schema:
                valid_data = schema(**loaded_data)
                return valid_data
        except :
            return None

if __name__ == "__main__":
  from LLM_Character.communication.incoming_messages import PromptMessage, SystemMessage
  from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher
  from LLM_Character.world.dispatchers.setup_dispatcher import SystemDispatcher

  dispatcher = MessageProcessor()

  json_string = '{"message": "hoi", "value": 1}'
  value = dispatcher.validate_data(json_string)
  assert value == None
  
  json_string = '{"type": "PromptMessage", "data": {"persona_name": "Camila", "message": "hoi", "value": 1}}'
  value = dispatcher.validate_data(json_string)
  assert isinstance(value, PromptMessage), f"it is somethign else {type(value)}"
