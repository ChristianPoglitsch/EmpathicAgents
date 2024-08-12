import sys
import json 
from typing import Type, Union
sys.path.append('../../')

from LLM_Character.world.validation_dataclass import BaseMessage
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher
from LLM_Character.world.dispatchers.system_dispatcher import SystemDispatcher
from LLM_Character.world.validation_dataclass import PromptMessage, SystemMessage
from LLM_Character.world.game import ReverieServer
from LLM_Character.llm_api import LLM_API
from LLM_Character.udp_comms import UdpComms

class MessageProcessor:
    def __init__(self):
        self._dispatch_map: dict[str, BaseDispatcher] = {}
        self._validator_map: dict[str, Type[BaseMessage]] = {}

        self.register('PromptMessage', PromptMessage, PromptDispatcher())
        self.register('SystemData', SystemMessage, SystemDispatcher())

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
  from LLM_Character.world.validation_dataclass import PromptMessage, SystemMessage
  from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher
  from LLM_Character.world.dispatchers.system_dispatcher import SystemDispatcher

  dispatcher = MessageProcessor()

  json_string = '{"message": "hoi", "value": 1}'
  value = dispatcher.validate_data(json_string)
  assert value == None
  
  json_string = '{"type": "PromptMessage", "data": {"persona_name": "Camila", "message": "hoi", "value": 1}}'
  value = dispatcher.validate_data(json_string)
  assert isinstance(value, PromptMessage), f"it is somethign else {type(value)}"
