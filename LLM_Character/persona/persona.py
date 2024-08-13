import sys
sys.path.append('../../')

from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.memory_structures.scratch.scratch import Scratch
from LLM_Character.world.validation_dataclass import PersonaData 

from LLM_Character.persona.cognitive_modules.plan import plan
from LLM_Character.persona.cognitive_modules.reflect import reflect
from LLM_Character.persona.cognitive_modules.converse import open_convo_session 

class Persona: 
  s_mem:MemoryTree
  a_mem:AssociativeMemory
  scratch:Scratch
  
  def __init__(self, name, folder_mem_saved:str):
    f_s_mem_saved = f"{folder_mem_saved}/spatial_memory.json"
    self.s_mem = MemoryTree(f_s_mem_saved)

    f_a_mem_saved = f"{folder_mem_saved}/associative_memory"
    self.a_mem = AssociativeMemory(f_a_mem_saved)

    scratch_saved = f"{folder_mem_saved}/scratch.json"
    self.scratch = Scratch(name, scratch_saved)
  
  @staticmethod
  def save_as(folder_mem_saved:str, data:PersonaData):
    f_s_mem_saved = f"{folder_mem_saved}/spatial_memory.json"
    MemoryTree.save_as(f_s_mem_saved, data.spatial_data)

    f_a_mem_saved = f"{folder_mem_saved}/associative_memory"
    AssociativeMemory.save_as(f_a_mem_saved, data.as_mem_data) 

    scratch_saved = f"{folder_mem_saved}/scratch.json"
    Scratch.save_as(scratch_saved, data.scratch_data)


  def save(self, save_folder): 
    f_s_mem = f"{save_folder}/spatial_memory.json"
    self.s_mem.save(f_s_mem)

    f_a_mem = f"{save_folder}/associative_memory"
    self.a_mem.save(f_a_mem)

    f_scratch = f"{save_folder}/scratch.json"
    self.scratch.save(f_scratch)

  def plan(self, new_day, model):
    return plan(self.scratch, self.a_mem, new_day, model)

  def reflect(self):
    reflect(self.scratch, self.a_mem)

  def move(self, personas, curr_location, curr_time):
    self.scratch.curr_location = curr_location

    new_day = False
    if not self.scratch.curr_time: 
      new_day = "First day"
    elif (self.scratch.curr_time.strftime('%A %B %d')
          != curr_time.strftime('%A %B %d')):
      new_day = "New day"
    self.scratch.curr_time = curr_time

    self.plan(personas, new_day)
    self.reflect()

  def open_convo_session(self, data, model) -> str: 
    return open_convo_session(self.scratch, data, model)












