"""
ibrahim: temporary class which will be replaced by the hungarian team?
# after all, they are going to use grpc, and so most of the socket programmming will dissapear
# no need to make it complicated for now, (assume single client single server), but the server (revererieserver) takes in client-id
# which makes it possible to run multiple instances for different clients without having a conflict.
"""

import json
from typing import Type, Union

from LLM_Character.communication.incoming_messages import (
    AddPersonaMessage,
    BaseMessage,
    GetMetaDataMessage,
    GetPersonaDetailsMessage,
    GetPersonasMessage,
    GetSavedGamesMessage,
    GetUsersMessage,
    MoveMessage,
    PromptMessage,
    StartMessage,
    UpdateMetaMessage,
    UpdatePersonaMessage,
    UpdateUserMessage,
)
from LLM_Character.communication.udp_comms import UdpComms
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.world.dispatchers.info_dispatcher import (
    GetMetaDataDispatcher,
    GetPersonaDetailsDispatcher,
    GetPersonasDispatcher,
    GetSavedGamesDispatcher,
    GetUsersDispatcher,
)
from LLM_Character.world.dispatchers.move_dispatcher import MoveDispatcher
from LLM_Character.world.dispatchers.persona_dispatcher import AddPersonaDispatcher
from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher
from LLM_Character.world.dispatchers.start_dispatcher import StartDispatcher
from LLM_Character.world.dispatchers.update_dispatcher import (
    UpdateMetaDispatcher,
    UpdatePersonaDispatcher,
    UpdateUserDispatcher,
)
from LLM_Character.world.game import ReverieServer


class MessageProcessor:
    def __init__(self):
        self._dispatch_map: dict[str, BaseDispatcher] = {}
        self._validator_map: dict[str, Type[BaseMessage]] = {}

        # POST/ PUT REQUESTS
        self.register("PromptMessage", PromptMessage, PromptDispatcher())
        self.register("StartMessage", StartMessage, StartDispatcher())
        self.register("UpdateUserMessage", UpdateUserMessage, UpdateUserDispatcher())
        self.register("UpdateMetaMessage", UpdateMetaMessage, UpdateMetaDispatcher())
        self.register(
            "UpdatePersonaMessage", UpdatePersonaMessage, UpdatePersonaDispatcher()
        )
        self.register("AddPersonaMessage", AddPersonaMessage, AddPersonaDispatcher())
        self.register("MoveMessage", MoveMessage, MoveDispatcher())

        # GET REQUESTS
        self.register("GetPersonasMessage", GetPersonasMessage, GetPersonasDispatcher())
        self.register("GetUsersMessage", GetUsersMessage, GetUsersDispatcher())
        self.register(
            "GetPersonaDetailsMessage",
            GetPersonaDetailsMessage,
            GetPersonaDetailsDispatcher(),
        )
        self.register(
            "GetSavedGamesMessage", GetSavedGamesMessage, GetSavedGamesDispatcher()
        )
        self.register("GetMetaDataMessage", GetMetaDataMessage, GetMetaDataDispatcher())

    def register(
        self,
        message_type: str,
        message_class: Type[BaseMessage],
        dispatcher_class: BaseDispatcher,
    ):
        self._validator_map[message_type] = message_class
        self._dispatch_map[message_type] = dispatcher_class

    def dispatch(
        self, socket: UdpComms, server: ReverieServer, model: LLM_API, data: BaseMessage
    ):
        # FIXME: call handler in seperate process.
        # threads arent usefull due to GIL
        # use a wroker - master architecture ...
        # maybe use indirect communication, like pub sub or
        # for example, RabbitMQ can be used with pub sub.
        self._dispatch_map[data.type.value].handler(socket, server, model, data)

    def validate_data(self, data: str) -> Union[BaseMessage, None]:
        try:
            loaded_data = json.loads(data)
            data_type = loaded_data.get("type")

            if not data_type:
                print("No 'type' field found in the data.")
                return None

            schema = self._validator_map.get(data_type)
            if not schema:
                print(f"No schema registered for message type: {data_type}")
                return None

            try:
                valid_data = schema(**loaded_data)
                return valid_data
            except TypeError as e:
                print(f"Validation failed due to a TypeError: {e}")
            except ValueError as e:
                print(f"Validation failed due to a ValueError: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during validation: {e}")

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    from LLM_Character.communication.incoming_messages import (
        PromptMessage,
    )
    from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher

    dispatcher = MessageProcessor()

    json_string = '{"message": "hoi", "value": 1}'
    value = dispatcher.validate_data(json_string)
    assert value is None

    json_string = '{"type": "PromptMessage", "data": {"persona_name": "Camila", "message": "hoi"}}'
    value = dispatcher.validate_data(json_string)
    assert isinstance(value, PromptMessage), f"it is somethign else {type(value)}"
