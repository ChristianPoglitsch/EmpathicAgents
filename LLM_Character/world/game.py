import datetime
import json 
import sys
sys.path.append('../')

from LLM_Character.persona.persona import Persona
from LLM_Character.llm_api import LLM_API 
from LLM_Character.world.utils import copyanything

from LLM_Character.world.validation import PromptMessage, SystemMessage
from LLM_Character.world.dispatchers.prompt_dispatcher import PromptDispatcher
from LLM_Character.world.dispatchers.system_dispatcher import SystemDispatcher
from LLM_Character.world.message_processor import MessageProcessor

# TODO move this variable to env file. 
FS_STORAGE = "LLM_Chracter/storage"

class ReverieServer:
  def __init__(self,
               fork_sim_code:str,
               sim_code:str):

    self.fork_sim_code = fork_sim_code
    self.sim_code = sim_code

    fork_folder = f"{FS_STORAGE}/{self.fork_sim_code}"
    sim_folder = f"{FS_STORAGE}/{self.sim_code}"

    copyanything(fork_folder, sim_folder)
    with open(f"{sim_folder}/reverie/meta.json") as json_file:  
      reverie_meta = json.load(json_file)

    with open(f"{sim_folder}/reverie/meta.json", "w") as outfile: 
      reverie_meta["fork_sim_code"] = fork_sim_code
      outfile.write(json.dumps(reverie_meta, indent=2))

    self.curr_time = datetime.datetime.strptime(reverie_meta['curr_time'], "%B %d, %Y, %H:%M:%S")
    self.sec_per_step = reverie_meta['sec_per_step']
    self.step = reverie_meta['step']

    self.personas:dict[str, Persona] = dict()
    for persona_name in reverie_meta['persona_names']: 
      persona_folder = f"{sim_folder}/personas/{persona_name}"
      curr_persona = Persona(persona_name, persona_folder)
      self.personas[persona_name] = curr_persona

  def save(self): 
    sim_folder = f"{FS_STORAGE}/{self.sim_code}"

    reverie_meta = dict() 
    reverie_meta["fork_sim_code"] = self.fork_sim_code
    reverie_meta["curr_time"] = self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
    reverie_meta["sec_per_step"] = self.sec_per_step
    reverie_meta["persona_names"] = list(self.personas.keys())
    reverie_meta["step"] = self.step
    reverie_meta_f = f"{sim_folder}/reverie/meta.json"
    with open(reverie_meta_f, "w") as outfile: 
      outfile.write(json.dumps(reverie_meta, indent=2))

    for persona_name, persona in self.personas.items(): 
      save_folder = f"{sim_folder}/personas/{persona_name}/bootstrap_memory"
      persona.save(save_folder)


  def start_server(self, sock):
    # sim_folder = f"{FS_STORAGE}/{self.sim_code}"

    dispatcher = MessageProcessor()
    dispatcher.register('PromptMessage', PromptMessage, PromptDispatcher)
    dispatcher.register('SystemData', SystemMessage, SystemDispatcher)

    while True:
      byte_data = sock.ReadReceivedData()
      if not byte_data:
          continue  

      value = dispatcher.validate_data(byte_data)
      if value is None:
          continue
      # NOTE:
      # unity sets the pace, do you have a seperate handler only for planning/reflecting that's possible
      # or if you want to have like a polling mechanism, where each time there is a converation request, you first execute plan/reflect is also possible. 
      dispatcher.dispatch(value)

        #     # TODO normally, you click on the unity character. so person_name should be provided in the byte_data message.
        #     # but we will hardcode it for now.
        #     # the same holds for information such as location., which is used in the else block of this code unit:  
        #     persona_name = "Camila"
        #     self.personas[persona_name].open_convo_session(sock, byte_data, "analysis")
        # else:
        #     movements = {"persona": dict(), 
        #                    "meta": dict()}
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
        #     self.step += 1
        #     self.curr_time += datetime.timedelta(seconds=self.sec_per_step)



if __name__ == "__main__" : 
  r = ReverieServer("ale", "tof")
  r.start_server(None)




