import datetime
import json 
import sys
sys.path.append('../../')

from LLM_Character.persona.persona import Persona
from LLM_Character.llm_api import LLM_API 
from LLM_Character.world.utils import copyanything
from LLM_Character.world.validation_dataclass import LocationData 

# TODO move this variable to env file. 
FS_STORAGE = "storage"

class ReverieServer:
  def __init__(self,
               fork_sim_code:str,
               sim_code:str):

    self.fork_sim_code = fork_sim_code
    self.sim_code = sim_code

    fork_folder = f"{FS_STORAGE}/{self.fork_sim_code}"
    sim_folder = f"{FS_STORAGE}/{self.sim_code}"

    copyanything(fork_folder, sim_folder)
    
    # TODO add a try and except when trying to load json...
    with open(f"{sim_folder}/meta.json") as json_file:  
      reverie_meta = json.load(json_file)

    with open(f"{sim_folder}/meta.json", "w") as outfile: 
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

    # sim_folder = f"{FS_STORAGE}/{self.sim_code}"

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


  def prompt_processor(self, persona_name:str):
    self.personas[persona_name].open_convo_session(socket, data.data.message)


  def update_processor(self, curr_location:dict[str, LocationData]):
    sim_folder = f"{FS_STORAGE}/{self.sim_code}"

    movements = { "persona": dict(), 
                  "meta": dict()}
    for persona_name, persona in self.personas.items(): 
      description = persona.move(self.personas, curr_location[persona_name], self.curr_time)  

      movements["persona"][persona_name] = {}
      movements["persona"][persona_name]["description"] = description
      movements["persona"][persona_name]["chat"] = (persona
                                              .scratch.chat)

    movements["meta"]["curr_time"] = (self.curr_time 
                                .strftime("%B %d, %Y, %H:%M:%S"))

    curr_move_file = f"{sim_folder}/movement/{self.step}.json"
    with open(curr_move_file, "w") as outfile: 
      outfile.write(json.dumps(movements, indent=2))
      
  # def system_processor():
  #   pass

# if __name__ == "__main__" : 
#   r = ReverieServer("ale", "tof")
#   r.start_server(None)




