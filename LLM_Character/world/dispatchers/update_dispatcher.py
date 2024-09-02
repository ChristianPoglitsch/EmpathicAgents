from LLM_Character.communication.incoming_messages import (
    UpdateMetaMessage,
    UpdatePersonaMessage,
    UpdateUserMessage,
)
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.communication.udp_comms import UdpComms
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher


class UpdateMetaDispatcher(BaseDispatcher):
    def handler(
        self,
        socket: UdpComms,
        serverM: ReverieServerManager,
        model: LLM_API,
        data: UpdateMetaMessage,
    ):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            server.update_meta_processor(data.data)
            print("Done")
            socket.SendData("Done")
        else:
            # FIXME: have proper error messages.
            socket.SendData("Error: Select a saved game first or start a new game.")


class UpdatePersonaDispatcher(BaseDispatcher):
    def handler(
        self,
        socket: UdpComms,
        serverM: ReverieServerManager,
        model: LLM_API,
        data: UpdatePersonaMessage,
    ):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            server.update_persona_processor(data.data)
            print("Done")
            socket.SendData("Done")
        else:
            socket.SendData("Error: Select a saved game first or start a new game.")


class UpdateUserDispatcher(BaseDispatcher):
    def handler(
        self,
        socket: UdpComms,
        serverM: ReverieServerManager,
        model: LLM_API,
        data: UpdateUserMessage,
    ):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            server.update_user_processor(data.data)
            print("Done")
            socket.SendData("Done")
        else:
            socket.SendData("Error: Select a saved game first or start a new game.")
