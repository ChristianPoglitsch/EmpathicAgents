"""
Plan new steps or quests.
"""

import sys
sys.path.append('../')

from persona import Persona
from LLM_Character.llm_api import LLM_API 

# TODO: make an export file, so you import all the function from one place, where you can index them. 
# so, import exportfile as prompt -> such that prompt.get_run_prompt_wake_up

from persona.prompt_templates.planning_prompts.wake_up import run_prompt_wake_up 
from persona.prompt_templates.planning_prompts.daily_plan import run_prompt_daily_plan

# NOTE time to fix this and just cut out the things that we dont need.
# for example, new_day we need that shi 
# long_term_planning, we need that shi
# even if we wont do any activity, it may be beneficial for the converation
# the conversation can take place anywhere in the planned schedule, 
# without it actually taken place. 
# for example, should_react, should go, since you will alayw be reacting, 
# youre always planning for a chat. 

def plan(persona:Persona, new_day:str, model:LLM_API): 
  if new_day:
    # NOTE we adjust persona scratch memory to add a new planning,
    # which includes, f_daily_schedule and daily_req 
    # f_daily_schedule_hourly_org etc.
    _long_term_planning(persona, new_day, model)

  if persona.scratch.act_check_finished():
    # NOTE we adjust persona scratch memory to add a new action,
    # which includes, act_event and act_object_event
    # from the task plannning that is stored also in scratch memory. 
    _determine_action(persona) 
  
  # NOTE no need for retrieved and should_react and chat_react, since you will always chat with the person talking. 
  # but if in the future there will be multiple NPC's, then it can be beneficial to re-add code here, see original repo.

  return persona.scratch.act_address


def _long_term_planning(persona, new_day, model): 
  wake_up_hour = generate_wake_up_hour(persona, model)

  if new_day == "First day": 
    persona.scratch.daily_req = generate_first_daily_plan(persona, wake_up_hour)

  elif new_day == "New day":
    revise_identity(persona, model)

  persona.scratch.f_daily_schedule = generate_hourly_schedule(persona, wake_up_hour)
  persona.scratch.f_daily_schedule_hourly_org = (persona.scratch.f_daily_schedule[:])

  thought = f"This is {persona.scratch.name}'s plan for {persona.scratch.curr_time.strftime('%A %B %d')}:"
  for i in persona.scratch.daily_req: 
    thought += f" {i},"
  thought = thought[:-1] + "."
  created = persona.scratch.curr_time
  expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
  s, p, o = (persona.scratch.name, "plan", persona.scratch.curr_time.strftime('%A %B %d'))
  keywords = set(["plan"])
  thought_poignancy = 5
  thought_embedding_pair = (thought, get_embedding(thought))
  persona.a_mem.add_thought(created, expiration, s, p, o, 
                            thought, keywords, thought_poignancy, 
                            thought_embedding_pair, None)

  # print("Sleeping for 20 seconds...")
  # time.sleep(10)
  # print("Done sleeping!")

def generate_wake_up_hour(persona, model):
  return int(run_prompt_wake_up(persona, model)[0])


def generate_first_daily_plan(persona, wake_up_hour): 
  return run_prompt_daily_plan(persona, wake_up_hour)[0]

def revise_identity(persona, model:LLM_API): 
  p_name = persona.scratch.name

  focal_points = [f"{p_name}'s plan for {persona.scratch.get_str_curr_date_str()}.",
                  f"Important recent events for {p_name}'s life."]
  retrieved = new_retrieve(persona, focal_points)

  statements = "[Statements]\n"
  for key, val in retrieved.items():
    for i in val: 
      statements += f"{i.created.strftime('%A %B %d -- %H:%M %p')}: {i.embedding_key}\n"

  # print (";adjhfno;asdjao;idfjo;af", p_name)
  plan_prompt = statements + "\n"
  plan_prompt += f"Given the statements above, is there anything that {p_name} should remember as they plan for"
  plan_prompt += f" *{persona.scratch.curr_time.strftime('%A %B %d')}*? "
  plan_prompt += f"If there is any scheduling information, be as specific as possible (include date, time, and location if stated in the statement)\n\n"
  plan_prompt += f"Write the response from {p_name}'s perspective."
  plan_note = model.send_text(plan_prompt)
  # print (plan_note)

  thought_prompt = statements + "\n"
  thought_prompt += f"Given the statements above, how might we summarize {p_name}'s feelings about their days up to now?\n\n"
  thought_prompt += f"Write the response from {p_name}'s perspective."
  thought_note = ChatGPT_single_request(thought_prompt)
  # print (thought_note)

  currently_prompt = f"{p_name}'s status from {(persona.scratch.curr_time - datetime.timedelta(days=1)).strftime('%A %B %d')}:\n"
  currently_prompt += f"{persona.scratch.currently}\n\n"
  currently_prompt += f"{p_name}'s thoughts at the end of {(persona.scratch.curr_time - datetime.timedelta(days=1)).strftime('%A %B %d')}:\n" 
  currently_prompt += (plan_note + thought_note).replace('\n', '') + "\n\n"
  currently_prompt += f"It is now {persona.scratch.curr_time.strftime('%A %B %d')}. Given the above, write {p_name}'s status for {persona.scratch.curr_time.strftime('%A %B %d')} that reflects {p_name}'s thoughts at the end of {(persona.scratch.curr_time - datetime.timedelta(days=1)).strftime('%A %B %d')}. Write this in third-person talking about {p_name}."
  currently_prompt += f"If there is any scheduling information, be as specific as possible (include date, time, and location if stated in the statement).\n\n"
  currently_prompt += "Follow this format below:\nStatus: <new status>"
  # print ("DEBUG ;adjhfno;asdjao;asdfsidfjo;af", p_name)
  # print (currently_prompt)
  new_currently = ChatGPT_single_request(currently_prompt)
  # print (new_currently)
  # print (new_currently[10:])

  persona.scratch.currently = new_currently

  daily_req_prompt = persona.scratch.get_str_iss() + "\n"
  daily_req_prompt += f"Today is {persona.scratch.curr_time.strftime('%A %B %d')}. Here is {persona.scratch.name}'s plan today in broad-strokes (with the time of the day. e.g., have a lunch at 12:00 pm, watch TV from 7 to 8 pm).\n\n"
  daily_req_prompt += f"Follow this format (the list should have 4~6 items but no more):\n"
  daily_req_prompt += f"1. wake up and complete the morning routine at <time>, 2. ..."

  new_daily_req = ChatGPT_single_request(daily_req_prompt)
  new_daily_req = new_daily_req.replace('\n', ' ')
  print ("WE ARE HERE!!!", new_daily_req)
  persona.scratch.daily_plan_req = new_daily_req

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
  
  # Step 1. Compressing the hourly schedule to the following format: 
  # The integer indicates the number of hours. They should add up to 24. 
  # [['sleeping', 6], ['waking up and starting her morning routine', 1], 
  # ['eating breakfast', 1], ['getting ready for the day', 1], 
  # ['working on her painting', 2], ['taking a break', 1], 
  # ['having lunch', 1], ['working on her painting', 3], 
  # ['taking a break', 2], ['working on her painting', 2], 
  # ['relaxing and watching TV', 1], ['going to bed', 1], ['sleeping', 2]]
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

  # Step 2. Expand to min scale (from hour scale)
  # [['sleeping', 360], ['waking up and starting her morning routine', 60], 
  # ['eating breakfast', 60],..
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

  # The goal of this function is to get us the action associated with 
  # <curr_index>. As a part of this, we may need to decompose some large 
  # chunk actions. 
  # Importantly, we try to decompose at least two hours worth of schedule at
  # any given point. 
  curr_index = persona.scratch.get_f_daily_schedule_index()
  curr_index_60 = persona.scratch.get_f_daily_schedule_index(advance=60)

  # * Decompose * 
  # During the first hour of the day, we need to decompose two hours 
  # sequence. We do that here. 
  if curr_index == 0:
    # This portion is invoked if it is the first hour of the day. 
    act_desp, act_dura = persona.scratch.f_daily_schedule[curr_index]
    if act_dura >= 60: 
      # We decompose if the next action is longer than an hour, and fits the
      # criteria described in determine_decomp.
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
    # If it is not the first hour of the day, this is always invoked (it is
    # also invoked during the first hour of the day -- to double up so we can
    # decompose two hours in one go). Of course, we need to have something to
    # decompose as well, so we check for that too. 
    if persona.scratch.curr_time.hour < 23:
      # And we don't want to decompose after 11 pm. 
      act_desp, act_dura = persona.scratch.f_daily_schedule[curr_index_60]
      if act_dura >= 60: 
        if determine_decomp(act_desp, act_dura): 
          persona.scratch.f_daily_schedule[curr_index_60:curr_index_60+1] = (
                              generate_task_decomp(persona, act_desp, act_dura))
  # * End of Decompose * 

  # Generate an <Action> instance from the action description and duration. By
  # this point, we assume that all the relevant actions are decomposed and 
  # ready in f_daily_schedule. 
  # print ("DEBUG LJSDLFSKJF")
  # for i in persona.scratch.f_daily_schedule: print (i)
  # print (curr_index)
  # print (len(persona.scratch.f_daily_schedule))
  # print (persona.scratch.name)
  # print ("------")


  # FIXME: what the hell is this? 
 
  # # 1440
  # x_emergency = 0
  # for i in persona.scratch.f_daily_schedule: 
  #   x_emergency += i[1]
  # # print ("x_emergency", x_emergency)
  #
  # if 1440 - x_emergency > 0: 
  #   print ("x_emergency__AAA", x_emergency)
  # persona.scratch.f_daily_schedule += [["sleeping", 1440 - x_emergency]]
  #
  #


  act_desp, act_dura = persona.scratch.f_daily_schedule[curr_index] 



  # Finding the target location of the action and creating action-related variables.
  #NOTE: voor nu zal de curr_location, gehardcoded worden.
  # so , spatial memory of the persona will contain all information about the location. No need for the maze object. 
  
  # Given (58, 9), 
  #     self.tiles[9][58] = {
  #           'world': 'double studio', 
  #           'sector': 'double studio', 
  #           'arena': 'bedroom 2', 
  #           'game_object': 'bed', 
  #           'spawning_location': 'bedroom-2-a', --> dont know what this is, i mean, not so important i assume.  
  #           'collision': False, --> has to do with front end, not important
 
              # NOTE: most import aspect of the tiles system is that it contains events. 
              # but since in our case, events will not be stored in tiles,
              # but sent on the basis of trigger detection and collision detection in unity. 
              # in the future, it means we dont need to store it here, which means we dont need it AT THIS MOMENT.  
  
  #           'events': {('double studio:double studio:bedroom 2:bed', None, None)}}  
  
  # FIXME: curr_location in persona needs to convert from using coordinates, to actually storing the dictionary as above. 
  act_world = persona.scratch.curr_location["world"]
  act_sector = persona.scratch.curr_tile["sector"]
  act_sector = generate_action_sector(act_desp, persona)
  act_arena = generate_action_arena(act_desp, persona, act_world, act_sector)
  act_address = f"{act_world}:{act_sector}:{act_arena}"
  
  act_game_object = generate_action_game_object(act_desp, act_address, persona)
  new_address = f"{act_world}:{act_sector}:{act_arena}:{act_game_object}"
  
  act_event = generate_action_event_triple(act_desp, persona)
  
  # Persona's actions also influence the object states. We set those up here. 
  # FIXME: state of object, being used or not, can be stored somehwere else, instead of tiles in maze. 
  # we can contruct for each object a class that stores this information or we cna query UNity. 
  # but for now, we can ignore this, it is out of scope for us.

  # Adding the action to persona's queue. 
  persona.scratch.add_new_action(new_address, 
                                 int(act_dura), 
                                 act_desp, 
                                 act_event,
                                 None,
                                 None,
                                 None,
                                 None)

def generate_action_sector(act_desp, persona): 
  return run_gpt_prompt_action_sector(act_desp, persona)[0]


def generate_action_arena(act_desp, persona, act_world, act_sector): 
  return run_gpt_prompt_action_arena(act_desp, persona, act_world, act_sector)[0]



def generate_action_game_object(act_desp, act_address, persona):
  if not persona.s_mem.get_str_accessible_arena_game_objects(act_address): 
    return "<random>"
  return run_gpt_prompt_action_game_object(act_desp, persona, act_address)[0]

