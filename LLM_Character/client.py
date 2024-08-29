import json
import time
from LLM_Character.communication.udp_comms import UdpComms

def temp(s) -> str:
    byte_data = None
    while True:
        time.sleep(1)
        byte_data = s.ReadReceivedData()
        if not byte_data:
            continue 
        break
    return byte_data
 

print("starting off ...")
udpIP="127.0.0.1"
portTX=8000
portRX=8001

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state waiting for late packets to arrive.
# s.bind() 

s = UdpComms(udpIP="127.0.0.1", portTX=8001, portRX=8000, enableRX=True, suppressWarnings=True)

json1 = {
        "type": "StartMessage",
        "data": {
            "fork_sim_code": "FORK123",
            "sim_code": "SIM456"
        }
    }

s.SendData(json.dumps(json1))
nice = temp(s)
print("Received1:")
print(nice)

json2 = {
    "type" : "PromptMessage",
    "data" : {
        "persona_name" : "Camila",
        "user_name" : "Louis",
        "message" : "Hi"
    }
}

s.SendData(json.dumps(json2))
nice = temp(s)
print("Received2:")
print(nice) 

# updateMetaJson = {
#     "curr_time": "July 25, 2024, 09:15:45",
#     "sec_per_step": 30
#     }

# updatePersonaJson  = {
#     "name" : "Camila", # old name
#     "scratch_data": {
#             "first_name": "Alice",
#             "last_name": "Smith",
#             "age": 30,
#             "living_area": {
#                     "world" : "Graz",
#                     "sector" : "DownTown",
#                     "arena" : "Someone's Appartement",
#             },
#             "recency_w": 5,
#             "relevance_w": 7,
#             "importance_ele_n": 3
#         },
#         "spatial_data": {
#             "FantasyLand" : {           
#                 "Northern Realm" : {
#                     "Dragon's Lair" : ["Dragon", "Treasure Chest"],
#                     "Ice Cavern" : ["Ice Golem" ,"Frozen Statue"]
#                 },
#                 "Southern Realm" :  {

#                 }
#             }
#         }
#     }

# updateUserJson = {
#     "old_name" : "Louis",
#     "name" : "Joe Smith",
# }

# json3 = {
#     "type" : "UpdateMetaMessage",
#     "data" : updateMetaJson 
# }

# json4 = {
#     "type" : "UpdatePersonaMessage",
#     "data" : updatePersonaJson
# }

# json5 = {
#     "type" : "UpdateUserMessage",
#     "data" : updateUserJson
# }

# s.SendData(json.dumps(json3))

# time.sleep(20)
# nice = s.ReadReceivedData()
# print("Received3:")
# print(nice) 

# s.SendData(json.dumps(json4))

# time.sleep(20)
# nice = s.ReadReceivedData()
# print("Received4:")
# print(nice) 

# s.SendData(json.dumps(json5))

# time.sleep(20)
# nice = s.ReadReceivedData()
# print("Received5:")
# print(nice) 

# AddPersonaJson  = {
#     "name" : "Alice Smith", # new name 
#     "scratch_data": {
#             "curr_location" : {
#                 "world" : "Graz",
#                 "sector" : "JakominiPlatz",
#                 "arena" : "Home"
#             },
#             "first_name": "Alice",
#             "last_name": "Smith",
#             "age": 30,
#             "innate": "Curious",
#             "learned": "Programming",
#             "currently": "Researcher",
#             "lifestyle": "Urban",
#             "living_area": {
#                     "world" : "Graz",
#                     "sector" : "DownTown",
#                     "arena" : "Someone's Appartement",
#             },
#             "recency_w": 5,
#             "relevance_w": 7,
#             "importance_w": 9,
#             "recency_decay": 2,
#             "importance_trigger_max": 10,
#             "importance_trigger_curr": 6,
#             "importance_ele_n": 3
#         },
#         "spatial_data": {
#             "FantasyLand": 
#             {
#                 "Northern Realm" : 
#                 {
#                     "Dragon's Lair" : ["Dragon", "Treasure Chest"],
#                     "Ice Cavern" : ["Ice Golem", "Frozen Statue"]
#                 }
#             }
#         }
#     }

# json6 = {
#     "type" : "AddPersonaMessage",
#     "data" : AddPersonaJson 
# }

# s.SendData(json.dumps(json6))

# time.sleep(20)
# nice = s.ReadReceivedData()
# print("Received6:")
# print(nice) 


MoveJson = {
    "world": "Graz",
    "sector": "JakominiPlatz",
    "arena" : "Bäckerei Sorger",
}

EventData1 = {
    "action_event_subject" : "Florian",
    "action_event_predicate" : None,
    "action_event_object" : None,
    "action_event_description" : None
#     "action_event_obj_subject" : "Hammer",
#     "action_event_obj_spredicate" : None,
#     "action_event_obj_sobject" : None,
#     "action_event_obj_sdescription" : None
}

json7 = {
    "type" : "MoveMessage",
    "data" : [{
        "name" : "Camila",
        "curr_loc" : MoveJson,
        "events" : [EventData1]
    }] 
}

s.SendData(json.dumps(json7))
nice = temp(s)
print("Received7:")
print(nice)

json8 = {
    "type" : "PromptMessage",
    "data" : {
        "persona_name" : "Camila",
        "user_name" : "Louis",
        "message" : "Hi"
    }
}
s.SendData(json.dumps(json8))

time.sleep(60)
nice = s.ReadReceivedData()
print("Received8:")
print(nice) 


# =============================================================================
# REQUESTING INFORMATION from unity endpoint to python endpoint  
# =============================================================================

json9 ={
    "type": "GetPersonasMessage",
    "data": None
}

s.SendData(json.dumps(json9))
nice = temp(s)
print("Received9:")
print(nice) 

json10 = {
    "type": "GetUsersMessage",
    "data": None
}

s.SendData(json.dumps(json10))
nice = temp(s)
print("Received10:")
print(nice) 

json11 = {
    "type": "GetPersonaDetailsMessage",
    "data": {
        "name": "example_name"
    }
}

s.SendData(json.dumps(json11))
nice = temp(s)
print("Received11:")
print(nice) 

json12 = {
    "type": "GetSavedGamesMessage",
    "data": None
}

s.SendData(json.dumps(json12))
nice = temp(s)
print("Received12:")
print(nice) 


json13 = {
    "type": "GetMetaDataMessage",
    "data": None
}

s.SendData(json.dumps(json13))
nice = temp(s)
print("Received13:")
print(nice) 
