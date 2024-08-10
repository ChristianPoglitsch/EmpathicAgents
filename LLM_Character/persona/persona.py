

from persona.memory_structures.spatial_memory import MemoryTree
from LLM_Character.persona.memory_structures.associative_memory import AssociativeMemory
from persona.memory_structures.scratch import Scratch

from persona.cognitive_modules.converse import *

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

  def save(self, save_folder): 
    f_s_mem = f"{save_folder}/spatial_memory.json"
    self.s_mem.save(f_s_mem)

    f_a_mem = f"{save_folder}/associative_memory"
    self.a_mem.save(f_a_mem)

    f_scratch = f"{save_folder}/scratch.json"
    self.scratch.save(f_scratch)

  def retrieve(self, perceived):
    return retrieve(self, perceived)

  def plan(self, maze, personas, new_day, retrieved):
    return plan(self, maze, personas, new_day, retrieved)

  def reflect(self):
    reflect(self)

  def move(self, personas, curr_location, curr_time):
    self.scratch.curr_location = curr_location

    new_day = False
    if not self.scratch.curr_time: 
      new_day = "First day"
    elif (self.scratch.curr_time.strftime('%A %B %d')
          != curr_time.strftime('%A %B %d')):
      new_day = "New day"
    self.scratch.curr_time = curr_time
    
    # FIXME: what does retrieve has as input ? i think previous chats? that's the only source of new information for the agent. 
    retrieved = self.retrieve(None)
    self.plan(maze, personas, new_day, retrieved)
    self.reflect()

    return 

  def open_convo_session(self, convo_mode): 
    open_convo_session(self, convo_mode)
    












  def open_convo_session(self, convo_mode): 
    open_convo_session(self, convo_mode)
