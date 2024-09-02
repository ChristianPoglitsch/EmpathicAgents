import json
import logging

import torch

from LLM_Character.communication.incoming_messages import (
    AddPersonaMessage,
    EventData,
    FullPersonaData,
    FullPersonaScratchData,
    GetMetaMessage,
    GetPersonaMessage,
    GetPersonasMessage,
    GetSavedGamesMessage,
    GetUsersMessage,
    MessageTypes,
    MetaData,
    MoveMessage,
    OneLocationData,
    PerceivingData,
    PersonaData,
    PersonaScratchData,
    PersonID,
    PromptData,
    PromptMessage,
    StartData,
    StartMessage,
    UpdateMetaMessage,
    UpdatePersonaMessage,
    UpdateUserMessage,
    UserData,
)
from LLM_Character.communication.message_processor import MessageProcessor
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.communication.udp_comms import UdpComms
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.llm_comms.llm_local import LocalComms
from LLM_Character.llm_comms.llm_openai import OpenAIComms
from LLM_Character.main import start_server
from LLM_Character.util import receive

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --------------------------------------------------------------------------------------
# START SERVER WITH THE FOLLOWING EXAMPLES USING OPENAI.
# --------------------------------------------------------------------------------------


def running_examples(client_sock: UdpComms, sim):
    start_mess = StartMessage(
        type=MessageTypes.STARTMESSAGE,
        data=StartData(fork_sim_code="FORK123", sim_code=sim))

    json1 = start_mess.model_dump_json()
    client_sock.SendData(json1)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    prompt_mess = PromptMessage(
        type=MessageTypes.PROMPTMESSAGE,
        data=PromptData(
            persona_name="Camila",
            user_name="Louis",
            message="hi"
        )
    )
    json2 = prompt_mess.model_dump_json()
    client_sock.SendData(json2)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    move_mess = MoveMessage(
        type=MessageTypes.MOVEMESSAGE,
        data=[PerceivingData(
            name="Camila",
            curr_loc=OneLocationData(
                world="Graz",
                sector="JakominiPlatz",
                arena="Bäckerei Sorger",
            ),
            events=[
                EventData(action_event_subject="Florian",
                          action_event_predicate=None,
                          action_event_object=None,
                          action_event_description=None)
            ]
        )]
    )

    json3 = move_mess.model_dump_json()
    client_sock.SendData(json3)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    update_meta_mess = UpdateMetaMessage(
        type=MessageTypes.UPDATE_META_MESSAGE,
        data=MetaData(
            curr_time="July 25, 2024, 09:15:45",
            sec_per_step=30
        ))

    json4 = update_meta_mess.model_dump_json()
    client_sock.SendData(json.dumps(json4))
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    update_persona_mess = UpdatePersonaMessage(
        type=MessageTypes.UPDATE_PERSONA_MESSAGE,
        data=PersonaData(
            name="Camila",
            scratch_data=PersonaScratchData(
                first_name="Alice",
                last_name="Smith",
                age=30,
                living_area=OneLocationData(
                    world="Graz",
                    sector="DownTown",
                    arena="Someone's Appartement"
                ),
                recency_w=5,
                relevance_w=7,
                importance_ele_n=3)
        ))

    json5 = update_persona_mess.model_dump_json()
    client_sock.SendData(json5)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    update_user_mess = UpdateUserMessage(
        type=MessageTypes.UPDATE_USER_MESSAGE,
        data=UserData(
            old_name="Louis",
            name="John Smith"
        )
    )

    json6 = update_user_mess.model_dump_json()
    client_sock.SendData(json6)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    add_persona_mess = AddPersonaMessage(
        type=MessageTypes.ADD_PERSONA_MESSAGE,
        data=FullPersonaData(
            name="Ahmed",
            scratch_data=FullPersonaScratchData(
                curr_location=OneLocationData(
                    world="Graz",
                    sector="JakominiPlatz",
                    arena="Home"
                ),
                first_name="Ahmed",
                last_name="El Bouzid",
                age=22,
                innate="Ahmed is brash, outspoken, and unapologetically blunt.\
                    His directness often crosses the line into vulgarity, \
                    and he's known for his requent use of coarse language. \
                    Despite his harsh exterior, there’s an underlying sense \
                    of loyalty and protectiveness towards those he cares about.",
                look="Ahmed has a robust build with a thick beard \
                    and a weathered face that reflects years of hard living. \
                    His hair is dark and usually kept short. He dresses in practical,\
                    often worn clothing that reflects his no-nonsense attitude.",
                learned="Ahmed grew up in a working-class neighborhood in Casablanca,\
                    where he learned the art of street smarts and survival. \
                    His education came from life experience rather than formal schooling.\
                    He picked up his extensive vocabulary of colorful language from \
                    the rough-and-tumble social circles he navigated. His bluntness \
                    and familiarity with vulgarity are as much a product of his environment\
                    as they are a personal choice.",
                currently="Ahmed is in Casablanca, sitting in a crowded, noisy café \
                    in the heart of the city. His presence is commanding, \
                    and he’s not shy about expressing his opinions loudly and colorfully.",
                lifestyle="Ahmed’s days are characterized by a blend of laborious work \
                    and boisterous socializing. He wakes up early to start his  \
                    day at the auto repair shop, where he tackles complex mechanical \
                    problems and interacts with a diverse clientele. After a hard \
                    day's work, he heads to his favorite local café, where he meets \
                    friends and engages in animated conversations. His language is \
                    as intense as his personality; he curses freely and speaks \
                    with a raw honesty that can be off-putting to some but is appreciated \
                    by those who value his straightforwardness. Evenings are \
                    typically spent at bustling marketplaces or local watering holes,\
                    where Ahmed's laughter and loud voice contribute to the vibrant \
                    atmosphere. His lifestyle is marked by a blend of hard work and \
                    a lively social life, punctuated by his unmistakable way of speaking.",
                living_area={
                    OneLocationData(
                        world="Graz",
                        sector="DownTown",
                        arena="Ahmed's Appartement"
                    )
                },
                recency_w=5,
                relevance_w=7,
                importance_w=9,
                recency_decay=2,
                importance_trigger_max=10,
                importance_trigger_curr=6,
                importance_ele_n=3
            ),
            spatial_data={
                "spatial_data": {
                    "FantasyLand":
                    {
                        "Northern Realm":
                        {
                            "Dragon's Lair": ["Dragon", "Treasure Chest"],
                            "Ice Cavern": ["Ice Golem", "Frozen Statue"]
                        }
                    }
                }
            }
        )
    )

    json7 = add_persona_mess.model_dump_json()
    client_sock.SendData(json7)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    get_personas_mess = GetPersonasMessage(
        type=MessageTypes.GET_PERSONAS_MESSAGE,
        data=None
    )
    json8 = get_personas_mess.model_dump_json()
    client_sock.SendData(json8)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    get_users_mess = GetUsersMessage(
        type=MessageTypes.GET_USERS_MESSAGE,
        data=None
    )
    json9 = get_users_mess.model_dump_json()
    client_sock.SendData(json9)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    get_persona_mess = GetPersonaMessage(
        type=MessageTypes.GET_PERSONA_MESSAGE,
        data=PersonID(
            name="Camila"
        )
    )
    json10 = get_persona_mess.model_dump_json()
    client_sock.SendData(json10)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    get_saved_games_mes = GetSavedGamesMessage(
        type=MessageTypes.GET_SAVED_GAMES_MESSAGE,
        data=None
    )

    json11 = get_saved_games_mes.model_dump_json()
    client_sock.SendData(json11)
    response = receive(client_sock)
    assert response is not None

    # ------------------------------------------

    get_meta_message = GetMetaMessage(
        type=MessageTypes.GET_META_MESSAGE,
        data=None
    )
    json12 = get_meta_message.model_dump_json()
    client_sock.SendData(json12)
    response = receive(client_sock)
    assert response is not None


if __name__ == "__main__":
    logging.INFO("CUDA found " + str(torch.cuda.is_available()))

    udpIP = "127.0.0.1"
    portTX = 9090
    portRX = 9091

    server_sock = UdpComms(
        udpIP=udpIP, portTX=portTX, portRX=portRX, enableRX=True, suppressWarnings=True
    )

    client_sock = UdpComms(
        udpIP=udpIP, portTX=portRX, portRX=portTX, enableRX=True, suppressWarnings=True
    )

    modelc = OpenAIComms()
    model_id = "gpt-4"
    modelc.init(model_id)
    model = LLM_API(modelc)

    dispatcher = MessageProcessor()
    server_manager = ReverieServerManager()

    start_server(server_sock, server_manager, dispatcher, model)
    running_examples(client_sock, "SIM456")

    # ------------------------------------------
    # other example, other port, other objects, but LocalLLM.
    # ------------------------------------------

    portTX = 8090
    portRX = 8081

    server_sock = UdpComms(
        udpIP=udpIP, portTX=portTX, portRX=portRX, enableRX=True, suppressWarnings=True
    )

    client_sock = UdpComms(
        udpIP=udpIP, portTX=portRX, portRX=portTX, enableRX=True, suppressWarnings=True
    )

    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc = LocalComms()
    modelc.init(model_id)
    model = LLM_API(modelc)

    dispatcher = MessageProcessor()
    server_manager = ReverieServerManager()

    running_examples(client_sock, "SIM123")
