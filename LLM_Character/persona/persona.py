import datetime
from typing import Tuple, Union

from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.persona.cognitive_modules.perceive import perceive
from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch 
from LLM_Character.communication.incoming_messages import FullPersonaData, FullPersonaScratchData, OneLocationData, PersonaScratchData

from LLM_Character.persona.cognitive_modules.plan import plan
from LLM_Character.persona.cognitive_modules.interact import interact
from LLM_Character.persona.cognitive_modules.reflect import reflect
from LLM_Character.persona.cognitive_modules.converse import chatting 


class Persona: 
  s_mem:MemoryTree
  a_mem:AssociativeMemory
  scratch:PersonaScratch
  
  def __init__(self, name):
    self.s_mem = MemoryTree()
    self.a_mem = AssociativeMemory()
    self.scratch = PersonaScratch(name)

  def load_from_file(self, folder_mem_saved:str):
    f_s_mem_saved = f"{folder_mem_saved}/spatial_memory.json"
    self.s_mem.load_from_file(f_s_mem_saved)

    f_a_mem_saved = f"{folder_mem_saved}/associative_memory"
    self.a_mem.load_from_file(f_a_mem_saved)

    scratch_saved = f"{folder_mem_saved}/scratch.json"
    self.scratch.load_from_file(scratch_saved)

  def load_from_data(self, scratch_data:FullPersonaScratchData, spatial_data):
    self.s_mem.load_from_data(spatial_data)
    self.scratch.load_from_data(scratch_data)

  def save(self, save_folder): 
    f_s_mem = f"{save_folder}/spatial_memory.json"
    self.s_mem.save(f_s_mem)

    f_a_mem = f"{save_folder}/associative_memory/"
    self.a_mem.save(f_a_mem)

    f_scratch = f"{save_folder}/scratch.json"
    self.scratch.save(f_scratch)

  def perceive(self, loc_data:OneLocationData, model:LLM_API):
    perceive(self.scratch, self.a_mem, self.s_mem, loc_data, model)
  
  def interacting(self):
    interact()

  def plan(self, new_day, model:LLM_API):
    return plan(self.scratch, self.a_mem, self.s_mem, new_day, model)

  def reflect(self, model:LLM_API):
    reflect(self.scratch, self.a_mem, model)

  def move(self, personas, curr_location:OneLocationData, curr_time:datetime.datetime, model:LLM_API):
    self.scratch.curr_location = curr_location.model_dump()
    
    new_day = False
    if not self.scratch.curr_time: 
      new_day = "First day"
    elif self.scratch.curr_time.strftime('%A %B %d') != curr_time.strftime('%A %B %d'):
      new_day = "New day"
    
    self.scratch.curr_time = curr_time
    
    self.perceive(curr_location, model)
    # self.retrieve_from_context() # or maybe inside perceive function
    self.plan(new_day, model)
    # self.interacting()    
    self.reflect(model)
    # self.execute() # inside unity.

  def open_convo_session(self, 
                        user_scratch:UserScratch, 
                        message:str,
                        curr_time:str,
                        model:LLM_API) -> Tuple[str, str, int]: 
    self.scratch.curr_time = curr_time
    return chatting(user_scratch, 
                    self.scratch, 
                    self.a_mem,
                    message,
                    model)

  def update_scratch(self, data: Union[PersonaScratchData, None]):
   if data : 
    self.scratch.update(data)

  def update_spatial(self, data) :
    if data: 
      self.s_mem.update_loc(data)


  def get_info(self) -> FullPersonaData:
    scratch_data = self.scratch.get_info()
    spatial_data = self.s_mem.get_info()
    data = FullPersonaData(name=self.scratch.name, scratch_data=scratch_data, spatial_data=spatial_data)
    return data 