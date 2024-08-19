import datetime
import json 
from typing import Tuple, Union 

from LLM_Character.persona.persona import Persona
from LLM_Character.persona.user import User 
from LLM_Character.llm_api import LLM_API 
from LLM_Character.util import copyanything, BASE_DIR
from LLM_Character.world.validation_dataclass import OneLocationData, SetupData 

FS_STORAGE = BASE_DIR + "/LLM_Character/storage"

# ------------------------
# FIXME: HOE ZORG JE ERVOOR DAT HET STATELESS MAAR DAT JE EERST SETUP MESSAGE UITVOERT EN DAN PAS MOVEMESSAGE OF PROMPTMESSAGE???
# IK DENK DAT IK EEN SERVER MANAGER OF IETS IN DIE SOORT NODIG ZAL HEBBEN. 
# want stel twee requests binnen met (verschillende of zelfde) sim_code ??? dan hebben we ook een probleem
# we moeten bijhouden wat er precies mogelijk is en wat niet.
# en de servermanager, is een dict van connection/socket -> reverieserver ? 
# ------------------------ 

class ReverieServer:
  def __init__(self,
               sim_code: str, 
               fork_sim_code:str = "default",
               cid:str = "localhost"):
      
    self.fork_sim_code = fork_sim_code
    self.sim_code = sim_code
    self.client_id = cid

  def loads(self):
    fork_folder = f"{FS_STORAGE}/{self.client_id}/{self.fork_sim_code}"
    sim_folder = f"{FS_STORAGE}/{self.client_id}/{self.sim_code}"

    # FIXME might raise exception, needs proper exception handling...
    copyanything(fork_folder, sim_folder)
    
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
    
    # NOTE its a single player game, so this can be adjusted to only one field of user, but for generality,
    # a dict has been chosen.
    self.users:dict[str, User] = dict()
    for user_name in reverie_meta['user_names']:
      curr_user = User(user_name)
      self.users[user_name] = curr_user

  def prompt_processor(self, user_name:str, persona_name:str, message:str, model:LLM_API) -> Tuple[str, str, int]:
    user = self.users[user_name]
    out = self.personas[persona_name].open_convo_session(user.scratch,
                                                          user.a_mem, 
                                                          message, 
                                                          self.curr_time,
                                                          model)
    self.curr_time += datetime.timedelta(seconds=self.sec_per_step)
    self.step += 1

    return out 


  def move_processor(self, curr_location:dict[str, OneLocationData]):
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
    
    self.curr_time += datetime.timedelta(seconds=self.sec_per_step)
    self.step += 1
    curr_move_file = f"{sim_folder}/movement/{self.step}.json"
    with open(curr_move_file, "w") as outfile: 
      outfile.write(json.dumps(movements, indent=2))

  
  def update_procesor(self, data: SetupData):
    self.save_as(data)
    self.sim_code = data.meta.sim_code
    sim_folder = f"{FS_STORAGE}/{self.sim_code}"
    
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

    self.users:dict[str, User] = dict()
    for user_name in reverie_meta['user_names']:
      user_folder = f"{sim_folder}/users/{user_name}"
      curr_user = User(user_name, user_folder)
      self.users[user_name] = curr_user
      
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
      save_folder = f"{sim_folder}/personas/{persona_name}/"
      Persona.save_as(save_folder, data.personas[persona_name])
    
    for user_name in data.meta.user_names: 
      save_folder = f"{sim_folder}/personas/{user_name}/"
      User.save_as(save_folder, data.users[user_name])

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



      
if __name__ == "__main__" :
  from example_data import example_update_message, example_setup_data
  r = ReverieServer()
  # FIXME niet content van de vorm van de data, door al die klas declaraties, 
  # kan het niet gedaan worden zonder? 
  r.loads(example_setup_data)
  r.prompt_processor("name", "message")
  r.update_processor(example_update_message)



