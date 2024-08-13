import sys
sys.path.append('../../')

from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch 
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.cognitive_modules.converse import chatting 

# User represents the human who plays the game.
class User: 
  a_mem:AssociativeMemory
  scratch:UserScratch
  def __init__(self, name:str, folder_mem_saved:str):

    f_a_mem_saved = f"{folder_mem_saved}/associative_memory"
    self.a_mem = AssociativeMemory(f_a_mem_saved)
    
    scratch_saved = f"{folder_mem_saved}/scratch.json"
    self.scratch = UserScratch(name, scratch_saved)

  def move(self, personas, curr_location, curr_time):
    self.scratch.curr_location = curr_location
    self.scratch.curr_time = curr_time
    self.reflect()

  def open_convo_session(self, data, model) -> str: 
    return chatting(self.scratch, data, model)



