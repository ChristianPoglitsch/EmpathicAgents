import datetime
import json 
import os
from typing import Tuple, Union 

from LLM_Character.persona.persona import Persona
from LLM_Character.persona.user import User 
from LLM_Character.llm_comms.llm_api import LLM_API 
from LLM_Character.util import copyanything, BASE_DIR
from LLM_Character.communication.incoming_messages import FullPersonaData, PerceivingData, MetaData, PersonID, PersonaData, UserData

FS_STORAGE = BASE_DIR + "/LLM_Character/storage"

class ReverieServer:
  def __init__(self,
               sim_code: str, 
               cid:str,
               fork_sim_code:str = "default",
               ):
      
    self.fork_sim_code = fork_sim_code
    self.sim_code = sim_code
    self.client_id = cid
    self.loaded = False 


  def is_loaded(self):
    # NOTE: or you could do os.path.isdir(sim_folder) 
    return self.loaded


  # =============================================================================
  # SECTION: Main Logic
  # =============================================================================
  
  def prompt_processor(self, user_name:str, persona_name:str, message:str, model:LLM_API) -> Tuple[str, str, int]:
    if self.loaded:
      user = self.users[user_name]
      out = self.personas[persona_name].open_convo_session(user.scratch,
                                                            message, 
                                                            self.curr_time,
                                                            model)
      self.curr_time += datetime.timedelta(seconds=self.sec_per_step)
      self.step += 1

      # autosave? 
      self._save()
      return out
    return None


  def move_processor(self, perceivements:list[PerceivingData], model:LLM_API):
    if self.loaded: 
      sim_folder = f"{FS_STORAGE}/{self.client_id}/{self.sim_code}"

      movements = { "persona": dict(), 
                    "meta": dict()}
      
      for p in perceivements: 
        if p.name in self.personas.keys():
          persona = self.personas[p.name]
          
          description = persona.move(self.personas, p.curr_loc, self.curr_time, model)  

          movements["persona"][p.name] = {}
          movements["persona"][p.name]["description"] = description
          movements["persona"][p.name]["chat"]        = persona.scratch.chat.prints_messages_sender()
        
      movements["meta"]["curr_time"] = self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
      
      self.curr_time += datetime.timedelta(seconds=self.sec_per_step)
      self.step += 1
      
      curr_move_file = f"{sim_folder}/movement/{self.step}.json"
      os.makedirs(os.path.dirname(curr_move_file), exist_ok=True)
      with open(curr_move_file, "w") as outfile: 
        outfile.write(json.dumps(movements, indent=2))
      
      # autosave ?
      self._save()

  def start_processor(self):
    self._load()


  def update_meta_processor(self, data: MetaData):
    if data.curr_time :
      # FIXME: proper error handling, make sure in the pydantic validation schema 
      # that data.curr_time conforms to the format "July 25, 2024, 09:15:45"  
      self.curr_time = datetime.datetime.strptime(data.curr_time, "%B %d, %Y, %H:%M:%S")
    if data.sec_per_step :
      self.sec_per_step = data.sec_per_step 
    
    # autosave? 
    self._save()


  def update_persona_processor(self, data : PersonaData):
    if data.name in self.personas.keys():
      persona = self.personas[data.name]
      persona.update_scratch(data.scratch_data)
      persona.update_spatial(data.spatial_data)
      # could be coded better, dont like this. 
      if data.scratch_data.living_area:
        persona.s_mem.update_oloc(data.scratch_data.living_area)
      if data.scratch_data.curr_location:
        persona.s_mem.update_oloc(data.scratch_data.curr_location)
    
    # autosave? 
    self._save()


  def update_user_processor(self, data : UserData):
    if data.old_name in self.users.keys():
      user = self.users.pop(data.old_name)
      # FIXME: not so good, law of demeter....
      user.scratch.name = data.name
      self.users[data.name] = user
    
    # autosave? 
    self._save()

  # TODO in every save function, if cannot be opned to write, make new dir and file 
  def add_persona_processor(self, data: FullPersonaData):
    if data.name not in self.personas.keys():
      p = Persona(data.name)
      p.load_from_data(data.scratch_data, data.spatial_data)
      # FIXME: not so good, law of demeter....
      p.scratch.curr_time = self.curr_time
      self.personas[data.name] = p

      # autosave? 
      self._save() 

  # =============================================================================
  # SECTION: Getters 
  # =============================================================================
  def get_personas(self) -> list[str]:
    return self.personas.keys()

  def get_users(self) -> list[str]:
    return self.users.keys()
  
  def get_persona_info(self, data:PersonID) -> Union[FullPersonaData, None]:
    if data.name in self.personas.keys():
      return self.personas[data.name].get_info()
    return None
  
  def get_meta_data(self) -> MetaData:
    return  MetaData(curr_time=self.curr_time.strftime("%B %d, %Y, %H:%M:%S"), sec_per_step=self.sec_per_step)
  
  def get_saved_games(self) -> list[str]:
    return os.listdir(f"{FS_STORAGE}/{self.client_id}/")   
  
  #  =============================================================================
  # SECTION: Loading and saving logic
  # =============================================================================


  def _load(self):
    fork_folder = f"{FS_STORAGE}/{self.client_id}/{self.fork_sim_code}"
    if not os.path.isdir(fork_folder):
      fork_folder = f"{FS_STORAGE}/localhost/default"

    # FIXME: check if sim folder doesnt already exist, otherwise return error.
    # or use that sim folder to load ? i guess the second.  
    sim_folder = f"{FS_STORAGE}/{self.client_id}/{self.sim_code}"
    if not os.path.isdir(sim_folder):
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
      curr_persona = Persona(persona_name)
      curr_persona.load_from_file(persona_folder)
      self.personas[persona_name] = curr_persona
    
    # NOTE its a single player game, so this can be adjusted to only one field of user, but for generality,
    # a dict has been chosen.
    self.users:dict[str, User] = dict()
    for user_name in reverie_meta['user_names']:
      curr_user = User(user_name)
      self.users[user_name] = curr_user
    
    self.loaded = True


  def _save(self):
    sim_folder = f"{FS_STORAGE}/{self.client_id}/{self.sim_code}"
    if self.loaded:
      reverie_meta = dict() 
      reverie_meta["fork_sim_code"] = self.fork_sim_code
      reverie_meta["curr_time"] = self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
      reverie_meta["sec_per_step"] = self.sec_per_step
      reverie_meta["persona_names"] = list(self.personas.keys())
      reverie_meta["user_names"] = list(self.users.keys())
      reverie_meta["step"] = self.step
      reverie_meta_f = f"{sim_folder}/meta.json"

      with open(reverie_meta_f, "w") as outfile: 
        outfile.write(json.dumps(reverie_meta, indent=2))

      for persona_name, persona in self.personas.items(): 
        save_folder = f"{sim_folder}/personas/{persona_name}"
        persona.save(save_folder)
  
      
if __name__ == "__main__" :
  from LLM_Character.persona.persona import Persona
  from LLM_Character.persona.user import User 
  from LLM_Character.llm_comms.llm_openai import OpenAIComms
  from LLM_Character.llm_comms.llm_local import LocalComms
  from LLM_Character.util import BASE_DIR
  import shutil 
  print("starting take off ...")
  
  # person = Persona("Camila", BASE_DIR + "/LLM_Character/storage/initial/personas/Camila")
  person = Persona("Florian", BASE_DIR + "/LLM_Character/storage/localhost/default/personas/Florian")
  user = User("Louis")
  
  # modelc = LocalComms()
  # model_id = "mistralai/Mistral-7B-Instruct-v0.2"
  # modelc.init(model_id)

  modelc = OpenAIComms()
  model_id = "gpt-4"
  modelc.init(model_id)

  model = LLM_API(modelc)
  message = "hi"
  
  r     = ReverieServer("sim_code", "notlocalhost")
  
  a     = r.is_loaded()
  out1  = r.prompt_processor(user.scratch.name, person.scratch.name, message, model)
  assert a == False
  assert out1 == None

  r.start_processor() 

  a     = r.is_loaded()
  out1  = r.prompt_processor(user.scratch.name, person.scratch.name, message, model)
  assert a == True 
  assert out1 != None 
  
 