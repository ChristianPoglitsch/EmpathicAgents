import socket
import sys
sys.path.append('../../')

from LLM_Character.world.validation import PromptMessage
from LLM_Character.world.dispatchers.dispatcher import BaseDispatcher
from LLM_Character.persona.persona import Persona

class PromptDispatcher(BaseDispatcher) : 
  def handler(self, data: PromptMessage, socket:socket.socket, personas:dict[str, Persona]):
    # TODO normally, you click on the unity character. so person_name should be provided in the byte_data message.
    # but we will hardcode it for now.
    # example: persona_name = data.data.persona_name
    persona_name = "Camila" 
    personas[persona_name].open_convo_session(socket, data.data.message)
        # else:
        #     movements = {"persona": dict(), 
        #                    "meta": dict()}

        #     # TODO normally, you click on the unity character. so person_name should be provided in the byte_data message.
        #     # but we will hardcode it for now.
        #     # the same holds for information such as location., which is used in the else block of this code unit:  
        #     # if it is a multi-character environment, then all names and all current location of those persona's should be sent as well. 
        #     persona_name = "Camila" 
        #     curr_location = {
        #         "World" : "Reverie"
        #         "Sector" : "Kortrijk"
        #         "Arena" : "begijnehof"
        #     }
        #    
        #     for persona_name, persona in self.personas.items(): 
        #         description = persona.move(self.personas, curr_location, self.curr_time)  
        #
        #         movements["persona"][persona_name] = {}
        #         movements["persona"][persona_name]["description"] = description
        #         movements["persona"][persona_name]["chat"] = (persona
        #                                                       .scratch.chat)
        #
        #     movements["meta"]["curr_time"] = (self.curr_time 
        #                                          .strftime("%B %d, %Y, %H:%M:%S"))
        #
        #     curr_move_file = f"{sim_folder}/movement/{self.step}.json"
        #     with open(curr_move_file, "w") as outfile: 
        #         outfile.write(json.dumps(movements, indent=2))
        #
