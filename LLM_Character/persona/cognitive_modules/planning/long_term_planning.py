import sys
import datetime
sys.path.append('../../../')

from persona import Persona
from LLM_Character.llm_api import LLM_API 
from LLM_Character.persona.cognitive_modules.retrieve import retrieve 
from LLM_Character.persona.prompt_modules.planning_prompts.long_term_planning.wake_up import run_prompt_wake_up 
from LLM_Character.persona.prompt_modules.planning_prompts.long_term_planning.wake_up import run_prompt_daily_plan
from LLM_Character.persona.prompt_modules.planning_prompts.long_term_planning.revise_identity  import run_prompt_revise_identity
from LLM_Character.persona.prompt_modules.planning_prompts.long_term_planning.hourly_schedule import run_prompt_hourly_schedule

def _long_term_planning(persona:Persona, new_day:str|None, model:LLM_API): 
  wake_up_hour = generate_wake_up_hour(persona, model)

  if new_day == "First day": 
    persona.scratch.daily_req = generate_first_daily_plan(persona, wake_up_hour)

  elif new_day == "New day":
    revise_identity(persona, model)

  persona.scratch.f_daily_schedule = make_hourly_schedule(persona, wake_up_hour)
  persona.scratch.f_daily_schedule_hourly_org = (persona.scratch.f_daily_schedule[:])
  
  (created, expiration,
  s, p, o, 
  thought, keywords, 
  thought_poignancy, thought_embedding_pair) = generate_thought_plan(persona, model)
  persona.a_mem.add_thought(created, expiration, s, p, o, 
                            thought, keywords, thought_poignancy, 
                            thought_embedding_pair, None)

def revise_identity(persona, model:LLM_API): 
  p_name = persona.scratch.name
  focal_points = [f"{p_name}'s plan for {persona.scratch.get_str_curr_date_str()}.",
                  f"Important recent events for {p_name}'s life."]

  retrieved = retrieve(persona, focal_points, model)
  _, _, new_currently, new_daily_req = run_prompt_revise_identity(persona, model, retrieved)

  persona.scratch.currently = new_currently
  persona.scratch.daily_plan_req = new_daily_req

#FIXME: try to make the code more readable instead of adding comments.  
def make_hourly_schedule(persona, wake_up_hour): 
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
          n_m1_activity += [generate_hourly_schedule(
                          persona, curr_hour_str, n_m1_activity, hour_str)]
  
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

def generate_thought_plan(persona:Persona, model:LLM_API):
  thought = f"This is {persona.scratch.name}'s plan for {persona.scratch.curr_time.strftime('%A %B %d')}:"
  for i in persona.scratch.daily_req: 
    thought += f" {i},"
  thought = thought[:-1] + "."
  
  created = persona.scratch.curr_time
  expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
  s, p, o = (persona.scratch.name, "plan", persona.scratch.curr_time.strftime('%A %B %d'))
  keywords = set(["plan"])
  thought_poignancy = 5
  thought_embedding_pair = (thought, model.semantic_meaning(thought))
  return created, expiration, s, p, o, thought, keywords, thought_poignancy, thought_embedding_pair 

def generate_wake_up_hour(persona, model):
  return int(run_prompt_wake_up(persona, model)[0])

def generate_first_daily_plan(persona, wake_up_hour): 
  return run_prompt_daily_plan(persona, wake_up_hour)[0]

def generate_hourly_schedule(persona, curr_hour_str, n_activity, hour_str):
  return run_prompt_hourly_schedule(persona, curr_hour_str, n_activity, hour_str)[0]

if __name__ == "__main__":
  from LLM_Character.llm_comms.llm_local import LocalComms
  person = Persona("BANDER", "filesave")
  modelc = LocalComms()
  model_id = "mistralai/Mistral-7B-Instruct-v0.2"
  modelc.init(model_id)

  model = LLM_API(modelc) 
  _long_term_planning(person, "First day",model)

