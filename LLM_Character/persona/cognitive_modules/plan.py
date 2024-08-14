"""
Plan new steps or quests.
"""

import sys

from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
sys.path.append('../../../')

from LLM_Character.llm_api import LLM_API 
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.cognitive_modules.planning.long_term_planning import _long_term_planning 
from LLM_Character.persona.cognitive_modules.planning.determine_action import _determine_action 

def plan(scratch:PersonaScratch, a_mem:AssociativeMemory, s_mem:MemoryTree, new_day:str, model:LLM_API): 
  if new_day:
    _long_term_planning(scratch, a_mem, new_day, model)

  if scratch.act_check_finished():
    _determine_action(scratch, s_mem, model) 
  
  return scratch.act_address

if __name__ == "__main__":
  from LLM_Character.persona.persona import Persona
  from llm_comms.llm_local import LocalComms
  
  person = Persona("MIKE")
  modelc = LocalComms()
  
  model_id = "mistralai/Mistral-7B-Instruct-v0.2"
  modelc.init(model_id)

  model = LLM_API(modelc)
  plan(person, "First Day", model)
