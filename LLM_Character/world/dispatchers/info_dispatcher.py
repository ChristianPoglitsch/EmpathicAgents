
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication.udp_comms import UdpComms
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.communication.incoming_messages import GetMetaDataMessage, GetPersonaDetailsMessage, GetPersonasMessage
from LLM_Character.communication.incoming_messages import GetSavedGamesMessage, GetUsersMessage
from LLM_Character.communication.outgoing_messages import GetMetaDataResponse, GetPersonaDetailsResponse, GetPersonasResponse
from LLM_Character.communication.outgoing_messages import GetSavedGamesResponse, GetUsersResponse


class GetMetaDataDispatcher(BaseDispatcher):
    def handler(
            self,
            socket: UdpComms,
            serverM: ReverieServerManager,
            model: LLM_API,
            data: GetMetaDataMessage):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            info = server.get_meta_data()
            response_message = GetMetaDataResponse(
                type="GetMetaDataResponse", data=info)
            sending_str = response_message.model_dump_json()

            print("Done")
            socket.SendData(sending_str)
        else:
            # FIXME: have proper error messages.
            socket.SendData(
                "Error: Select a saved game first or start a new game.")


class GetPersonaDetailsDispatcher(BaseDispatcher):
    def handler(
            self,
            socket: UdpComms,
            serverM: ReverieServerManager,
            model: LLM_API,
            data: GetPersonaDetailsMessage):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            info = server.get_persona_info(data.data)
            if info:
                response_message = GetPersonaDetailsResponse(
                    type="GetPersonaDetailsResponse", data=info)
                sending_str = response_message.model_dump_json()

                print("Done")
                socket.SendData(sending_str)
            else:
                socket.SendData("Error: Persona name doesn't exist.")
        else:
            # FIXME: have proper error messages.
            socket.SendData(
                "Error: Select a saved game first or start a new game.")


class GetPersonasDispatcher(BaseDispatcher):
    def handler(
            self,
            socket: UdpComms,
            serverM: ReverieServerManager,
            model: LLM_API,
            data: GetPersonasMessage):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            info = server.get_personas()
            response_message = GetPersonasResponse(
                type="GetPersonasResponse", data=info)
            sending_str = response_message.model_dump_json()

            print("Done")
            socket.SendData(sending_str)
        else:
            # FIXME: have proper error messages.
            socket.SendData(
                "Error: Select a saved game first or start a new game.")


class GetUsersDispatcher(BaseDispatcher):
    def handler(
            self,
            socket: UdpComms,
            serverM: ReverieServerManager,
            model: LLM_API,
            data: GetSavedGamesMessage):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            info = server.get_saved_games()
            response_message = GetSavedGamesResponse(
                type="GetSavedGamesResponse", data=info)
            sending_str = response_message.model_dump_json()

            print("Done")
            socket.SendData(sending_str)
        else:
            # FIXME: have proper error messages.
            socket.SendData(
                "Error: Select a saved game first or start a new game.")


class GetSavedGamesDispatcher(BaseDispatcher):
    def handler(
            self,
            socket: UdpComms,
            serverM: ReverieServerManager,
            model: LLM_API,
            data: GetUsersMessage):
        client_id = socket.udpIP + str(socket.udpSendPort)
        server = serverM.get_server(client_id)
        if server and server.is_loaded():
            info = server.get_users()
            response_message = GetUsersResponse(
                type="GetUsersResponse", data=info)
            sending_str = response_message.model_dump_json()

            print("Done")
            socket.SendData(sending_str)
        else:
            # FIXME: have proper error messages.
            socket.SendData(
                "Error: Select a saved game first or start a new game.")
