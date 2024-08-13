import datetime
import json 
import sys
from typing import Union 
sys.path.append('../../')

from LLM_Character.persona.persona import Persona
from LLM_Character.llm_api import LLM_API 
from LLM_Character.util import copyanything
from LLM_Character.world.validation_dataclass import OneLocationData, SetupData 

# TODO move this variable to env file. 
FS_STORAGE = "storage"

class ReverieServer:
  def __init__(self,
               fork_sim_code: Union[str, None] = None,
               sim_code: Union[str, None] = None):
    # NOTE if data is loaded from database and not from unity.
    if fork_sim_code or sim_code :
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

  def loads(self, data: SetupData):
    self.save_as(data)
    self.sim_code = data.meta.sim_code
    sim_folder = f"{FS_STORAGE}/{self.sim_code}"
    
    # TODO add a try and except when trying to load json...
    with open(f"{sim_folder}/meta.json") as json_file:  
      reverie_meta = json.load(json_file)

    self.curr_time = datetime.datetime.strptime(reverie_meta['curr_time'], "%B %d, %Y, %H:%M:%S")
    self.sec_per_step = reverie_meta['sec_per_step']
    self.step = reverie_meta['step']
    
    self.personas:dict[str, Persona] = dict()
    for persona_name in reverie_meta['persona_names']: 
      persona_folder = f"{sim_folder}/personas/{persona_name}"
      curr_persona = Persona(persona_name, persona_folder)
      self.personas[persona_name] = curr_persona

  def save_as(self, data: SetupData): 
    sim_folder = f"{FS_STORAGE}/{data.meta.sim_code}"

    reverie_meta = dict() 
    reverie_meta["fork_sim_code"] = data.meta.fork_sim_code 
    reverie_meta["curr_time"] = data.meta.curr_time
    reverie_meta["sec_per_step"] = data.meta.sec_per_step
    reverie_meta["persona_names"] = data.meta.persona_names
    reverie_meta["step"] = data.meta.step

    reverie_meta_f = f"{sim_folder}/reverie/meta.json"
    with open(reverie_meta_f, "w") as outfile: 
      outfile.write(json.dumps(reverie_meta, indent=2))

    for persona_name in data.meta.persona_names : 
      save_folder = f"{sim_folder}/personas/{persona_name}/bootstrap_memory"
      Persona.save_as(save_folder, data.personas[persona_name])

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


  def prompt_processor(self, persona_name:str, message:str, model:LLM_API) -> str:
    return self.personas[persona_name].open_convo_session(message, model)
    #FIXME: could be dispabled, to not increase time while chatting, or you could, idk which one is better.  
    # self.step += 1
    # self.curr_time += datetime.timedelta(seconds=self.sec_per_step)



  def update_processor(self, curr_location:dict[str, OneLocationData]):
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
      
if __name__ == "__main__" :
  from example_data import example_update_message, example_setup_data
  r = ReverieServer()
  # FIXME niet content van de vorm van de data, door al die klas declaraties, 
  # kan het niet gedaan worden zonder? 
  r.loads(example_setup_data)
  r.prompt_processor("name", "message")
  r.update_processor(example_update_message)



