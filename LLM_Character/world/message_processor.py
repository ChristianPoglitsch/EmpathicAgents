import json 

from LLM_Character.world.validation import BaseMessage
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher

import sys
sys.path.append('../')


class MessageProcessor:
    def __init__(self):
        self._dispatch_map: dict[str, BaseDispatcher] = {}
        self._validator_map: dict[str, BaseMessage] = {}

    def register(self, message_type: str, message_class, dispatcher_class):
        self._validator_map[message_type] = message_class
        self._dispatch_map[message_type] = dispatcher_class 

    def dispatch(self, data:BaseMessage):
      self._dispatch_map[data.type].handler(data)  

    def validate_data(self, data: str) -> BaseMessage | None:
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
  from LLM_Character.world.validation import PromptMessage, SystemMessage
  from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher
  from LLM_Character.world.dispatchers.system_dispatcher import SystemDispatcher

  dispatcher = MessageProcessor()
  dispatcher.register('PromptMessage', PromptMessage, PromptDispatcher)
  dispatcher.register('SystemData', SystemMessage, SystemDispatcher)

  json_string = '{"message": "hoi", "value": 1}'
  value = dispatcher.validate_data(json_string)
  assert value == None
  
  json_string = '{"type": "PromptMessage", "data": {"message": "hoi", "value": 1}}'
  value = dispatcher.validate_data(json_string)
  assert isinstance(value, PromptMessage)
