"""
Plan new steps or quests.
"""

import sys
sys.path.append('../../../')

from LLM_Character.llm_api import LLM_API 

from LLM_Character.persona.cognitive_modules.planning.long_term_planning import _long_term_planning 
from LLM_Character.persona.cognitive_modules.planning.determine_action import _determine_action 

def plan(persona, new_day:str, model:LLM_API): 
  if new_day:
    _long_term_planning(persona, new_day, model)

  if persona.scratch.act_check_finished():
    _determine_action(persona) 
  
  return persona.scratch.act_address

if __name__ == "__main__":
  from LLM_Character.persona.persona import Persona
  from llm_comms.llm_local import LocalComms
  
  person = Persona("MIKE")
  modelc = LocalComms()
  
  model_id = "mistralai/Mistral-7B-Instruct-v0.2"
  modelc.init(model_id)

  model = LLM_API(modelc)
  plan(person, "First Day", model)
