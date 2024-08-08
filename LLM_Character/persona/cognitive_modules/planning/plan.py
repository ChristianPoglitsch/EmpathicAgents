"""
Plan new steps or quests.
"""

import sys
sys.path.append('../../')

from persona import Persona
from LLM_Character.llm_api import LLM_API 


from persona.cognitive_modules.plan import _long_term_planning 

def plan(persona:Persona, new_day:str, model:LLM_API): 
  if new_day:
    _long_term_planning(persona, new_day, model)

  if persona.scratch.act_check_finished():
    _determine_action(persona) 
  
  return persona.scratch.act_address


def generate_hourly_schedule(persona, wake_up_hour): 
  hour_str = ["00:00 AM", "01:00 AM", "02:00 AM", "03:00 AM", "04:00 AM", 
              "05:00 AM", "06:00 AM", "07:00 AM", "08:00 AM", "09:00 AM", 
              "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM", 
              "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM", "07:00 PM",
              "08:00 PM", "09:00 PM", "10:00 PM", "11:00 PM"]
  n_m1_activity = []
  diversity_repeat_count = 3
  for i in range(diversity_repeat_count): 
    n_m1_activity_set = set(n_m1_activity)
    if len(n_m1_activity_set) < 5: 
      n_m1_activity = []
      for count, curr_hour_str in enumerate(hour_str): 
        if wake_up_hour > 0: 
          n_m1_activity += ["sleeping"]
          wake_up_hour -= 1
        else: 
          n_m1_activity += [run_gpt_prompt_generate_hourly_schedule(
                          persona, curr_hour_str, n_m1_activity, hour_str)[0]]
  
  _n_m1_hourly_compressed = []
  prev = None 
  prev_count = 0
  for i in n_m1_activity: 
    if i != prev:
      prev_count = 1 
      _n_m1_hourly_compressed += [[i, prev_count]]
      prev = i
    else: 
      if _n_m1_hourly_compressed: 
        _n_m1_hourly_compressed[-1][1] += 1

  n_m1_hourly_compressed = []
  for task, duration in _n_m1_hourly_compressed: 
    n_m1_hourly_compressed += [[task, duration*60]]

  return n_m1_hourly_compressed

def generate_task_decomp(persona, task, duration): 
  return run_gpt_prompt_task_decomp(persona, task, duration)[0]


def _determine_action(persona): 
  def determine_decomp(act_desp, act_dura):
    if "sleep" not in act_desp and "bed" not in act_desp: 
      return True
    elif "sleeping" in act_desp or "asleep" in act_desp or "in bed" in act_desp:
      return False
    elif "sleep" in act_desp or "bed" in act_desp: 
      if act_dura > 60: 
        return False
    return True

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
  
  # FIXME: state of object, being used or not, can be stored somehwere else, instead of tiles in maze. 
  # we can contruct for each object a class that stores this information or we cna query UNity. 
  # but for now, we can ignore this, it is out of scope for us.

  persona.scratch.add_new_action(new_address, 
                                 int(act_dura), 
                                 act_desp, 
                                 act_event)

def generate_action_sector(act_desp, persona): 
  return run_gpt_prompt_action_sector(act_desp, persona)[0]

def generate_action_arena(act_desp, persona, act_world, act_sector): 
  return run_gpt_prompt_action_arena(act_desp, persona, act_world, act_sector)[0]

def generate_action_game_object(act_desp, act_address, persona):
  if not persona.s_mem.get_str_accessible_arena_game_objects(act_address): 
    return "<random>"
  return run_gpt_prompt_action_game_object(act_desp, persona, act_address)[0]

def generate_action_event_triple(act_desp, persona): 
  return run_gpt_prompt_event_triple(act_desp, persona)[0]


