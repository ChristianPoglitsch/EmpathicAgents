"""
Plan new steps or quests.
"""

import sys
sys.path.append('../../')

from persona import Persona
from LLM_Character.llm_api import LLM_API 

from LLM_Character.persona.cognitive_modules.planning.long_term_planning import _long_term_planning 
from LLM_Character.persona.cognitive_modules.planning.determine_action import _determine_action 

def plan(persona:Persona, new_day:str, model:LLM_API): 
  if new_day:
    _long_term_planning(persona, new_day, model)

  if persona.scratch.act_check_finished():
    _determine_action(persona) 
  
  return persona.scratch.act_address


