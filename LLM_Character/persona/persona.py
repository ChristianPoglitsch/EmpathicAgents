

from persona.memory_structures.spatial_memory import MemoryTree
from LLM_Character.persona.memory_structures.associative_memory import AssociativeMemory
from persona.memory_structures.scratch import Scratch


class Persona: 
  s_mem:MemoryTree
  a_mem:AssociativeMemory
  scratch:Scratch
  
  def __init__(self, name, folder_mem_saved=False):
    # PERSONA BASE STATE 
    self.name = name
 
    # PERSONA MEMORY 
    f_s_mem_saved = f"{folder_mem_saved}/spatial_memory.json"
    self.s_mem = MemoryTree(f_s_mem_saved)

    f_a_mem_saved = f"{folder_mem_saved}/associative_memory"
    self.a_mem = AssociativeMemory(f_a_mem_saved)

    scratch_saved = f"{folder_mem_saved}/scratch.json"
    self.scratch = Scratch(scratch_saved)
