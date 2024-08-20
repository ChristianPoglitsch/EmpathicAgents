import datetime
import json 
import os
from typing import Tuple, Union 

from LLM_Character.persona.persona import Persona
from LLM_Character.persona.user import User 
from LLM_Character.llm_comms.llm_api import LLM_API 
from LLM_Character.util import copyanything, BASE_DIR
from LLM_Character.communication.incoming_messages import OneLocationData, UpdateData  

FS_STORAGE = BASE_DIR + "/LLM_Character/storage"


# TODO: 
  # FIXME: niet 1 update processor
  # maar meerdere en zeer specifiek. 
  # dus 1tje om scratch te veranderen van eeen bestaande persona, dus je moet persona naam al doorsturen. 
  # en 1tje om meta file te veranderen , maar daarvan kun je enkel curr_time veranderne , 
  # de usernames en personanames MAG JE NIET VERANDEREN !!!!!
  # die verander je door een andere functie weeral toe te voegen 
  # add persona to game 
  # remove persona to game
  # etc. 


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
    """ shouldnt be executed if the server is not loaded yet. """
    if self.loaded:
      user = self.users[user_name]
      out = self.personas[persona_name].open_convo_session(user.scratch,
                                                            message, 
                                                            self.curr_time,
                                                            model)
      self.curr_time += datetime.timedelta(seconds=self.sec_per_step)
      self.step += 1
      return out 
    return None


  def move_processor(self, curr_location:dict[str, OneLocationData]):
    """ shouldnt be executed if the server is not loaded yet. """
    if self.loaded: 
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


  def start_processor(self):
    self._load()

  # FIXME: niet 1 update processor
  # maar meerdere en zeer specifiek. 
  # dus 1tje om scratch te veranderen van eeen bestaande persona, dus je moet persona naam al doorsturen. 
  # en 1tje om meta file te veranderen , maar daarvan kun je enkel curr_time veranderne , 
  # de usernames en personanames MAG JE NIET VERANDEREN !!!!!
  # die verander je door een andere functie weeral toe te voegen 
  # add persona to game 
  # remove persona to game
  # etc. 
  def update_processor(self, data: UpdateData):
    """ shouldnt be executed if the server is not loaded yet. """
    self._save()
    self._save_as(data)
    self._load()

  # =============================================================================
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
      curr_persona = Persona(persona_name, persona_folder)
      self.personas[persona_name] = curr_persona
    
    # NOTE its a single player game, so this can be adjusted to only one field of user, but for generality,
    # a dict has been chosen.
    self.users:dict[str, User] = dict()
    for user_name in reverie_meta['user_names']:
      curr_user = User(user_name)
      self.users[user_name] = curr_user
    
    self.loaded = True


  def _save_as(self, data: UpdateData): 
    sim_folder = f"{FS_STORAGE}/{self.client_id}/{self.sim_code}"
    if self.loaded and data.meta:
      reverie_meta_f = f"{sim_folder}/meta.json"
      
      with open(reverie_meta_f, "r") as infile:
        reverie_meta = json.load(infile)    
      
      if data.meta.curr_time: 
        reverie_meta["curr_time"] = data.meta.curr_time
      if data.meta.sec_per_step:
        reverie_meta["sec_per_step"] = data.meta.sec_per_step
      if data.meta.persona_names:
        reverie_meta["persona_names"] = data.meta.persona_names
      if data.meta.step :
        reverie_meta["step"] = data.meta.step

      with open(reverie_meta_f, "w") as outfile: 
        outfile.write(json.dumps(reverie_meta, indent=2))

      for persona_name in data.meta.persona_names : 
        save_folder = f"{sim_folder}/personas/{persona_name}/"
        Persona.save_as(save_folder, data.personas[persona_name])
      
      for user_name in data.meta.user_names: 
        save_folder = f"{sim_folder}/personas/{user_name}/"
        User.save_as(save_folder, data.users[user_name])


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
  
  
  data_dict = {
    "meta" : None,
    "personas" : None,
    "users": None,
  }
  update_data_instance = UpdateData(**data_dict)
  out2  = r.update_processor(update_data_instance)

  data_dict = {
    "meta": {
        "curr_time": "2024-08-20T12:00:00Z",
        "sec_per_step": 30,
        "persona_names": ["John Doe", "Jane Smith"],
        "step": 5
    },
    "personas": {
        "john_doe": {
            "scratch_data": {
                "curr_time": "2024-08-20T12:00:00Z",
                "name": "John Doe",
                "age": 30
            },
            "spatial_data": None
        }
    },
    "users": {
        "jane_smith": {
            "scratch_data": {
                "name": "Jane Smith"
            }
        }
    }
  }

  update_data_instance = UpdateData(**data_dict)
  out2  = r.update_processor(update_data_instance)


  # shutil.rmtree( BASE_DIR + "/LLM_Character/storage/notlocalhost")
  # del r