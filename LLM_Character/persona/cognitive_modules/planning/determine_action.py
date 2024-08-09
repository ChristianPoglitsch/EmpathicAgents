
import sys
sys.path.append('../../')

from persona import Persona
from LLM_Character.llm_api import LLM_API 

import LLM_Character.persona.prompt_templates.planning_prompts.determine_action as p

def _determine_action(persona): 
  curr_index = persona.scratch.get_f_daily_schedule_index()
  curr_index_60 = persona.scratch.get_f_daily_schedule_index(advance=60)

  if curr_index == 0:
    act_desp, act_dura = persona.scratch.f_daily_schedule[curr_index]
    if act_dura >= 60: 
      if determine_decomp(act_desp, act_dura): 
        persona.scratch.f_daily_schedule[curr_index:curr_index+1] = (
          generate_task_decomp(persona, act_desp, act_dura))

    if curr_index_60 + 1 < len(persona.scratch.f_daily_schedule):
      act_desp, act_dura = persona.scratch.f_daily_schedule[curr_index_60+1]
      if act_dura >= 60: 
        if determine_decomp(act_desp, act_dura): 
          persona.scratch.f_daily_schedule[curr_index_60+1:curr_index_60+2] = (
            generate_task_decomp(persona, act_desp, act_dura))

  if curr_index_60 < len(persona.scratch.f_daily_schedule):
    if persona.scratch.curr_time.hour < 23:
      act_desp, act_dura = persona.scratch.f_daily_schedule[curr_index_60]
      if act_dura >= 60: 
        if determine_decomp(act_desp, act_dura): 
          persona.scratch.f_daily_schedule[curr_index_60:curr_index_60+1] = (
                              generate_task_decomp(persona, act_desp, act_dura))

  act_desp, act_dura = persona.scratch.f_daily_schedule[curr_index] 

  # FIXME: curr_location in persona needs to convert from using coordinates, to actually storing the dictionary as above. 
  act_world = persona.scratch.curr_location["world"]
  act_sector = persona.scratch.curr_tile["sector"]
  act_sector = generate_action_sector(act_desp, persona)

  act_arena = generate_action_arena(act_desp, persona, act_world, act_sector)
  act_address = f"{act_world}:{act_sector}:{act_arena}"
  
  act_game_object = generate_action_game_object(act_desp, act_address, persona)
  new_address = f"{act_world}:{act_sector}:{act_arena}:{act_game_object}"
  
  act_event = generate_action_event_triple(act_desp, persona)

  persona.scratch.add_new_action(new_address, 
                                 int(act_dura), 
                                 act_desp, 
                                 act_event)

def determine_decomp(act_desp, act_dura):
  if "sleep" not in act_desp and "bed" not in act_desp: 
    return True
  elif "sleeping" in act_desp or "asleep" in act_desp or "in bed" in act_desp:
    return False
  elif "sleep" in act_desp or "bed" in act_desp: 
    if act_dura > 60: 
      return False
  return True

def generate_task_decomp(persona, task, duration): 
  return p.run_prompt_task_decomp(persona, task, duration)[0]

def generate_action_sector(act_desp, persona): 
  return run_prompt_action_sector(act_desp, persona)[0]

def generate_action_arena(act_desp, persona, act_world, act_sector): 
  return run_prompt_action_arena(act_desp, persona, act_world, act_sector)[0]

def generate_action_game_object(act_desp, act_address, persona):
  if not persona.s_mem.get_str_accessible_arena_game_objects(act_address): 
    return "<random>"
  return run_prompt_action_game_object(act_desp, persona, act_address)[0]

def generate_action_event_triple(act_desp, persona): 
  return run_prompt_event_triple(act_desp, persona)[0]

if __name__ == "__main__":
  p = Persona("IBI")
  _determine_action(p)



