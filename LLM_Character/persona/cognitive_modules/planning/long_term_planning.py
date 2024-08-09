import sys
sys.path.append('../../../')

from persona import Persona
from LLM_Character.llm_api import LLM_API 

from LLM_Character.persona.prompt_modules.planning_prompts.long_term_planning.wake_up import run_prompt_wake_up 
from LLM_Character.persona.prompt_modules.planning_prompts.long_term_planning.wake_up import run_prompt_daily_plan
from LLM_Character.persona.prompt_modules.planning_prompts.long_term_planning.revise_identity  import run_prompt_revise_identity

def _long_term_planning(persona, new_day, model:LLM_API): 
  wake_up_hour = generate_wake_up_hour(persona, model)

  if new_day == "First day": 
    persona.scratch.daily_req = generate_first_daily_plan(persona, wake_up_hour)

  elif new_day == "New day":
    revise_identity(persona, model)

  persona.scratch.f_daily_schedule = generate_hourly_schedule(persona, wake_up_hour)
  persona.scratch.f_daily_schedule_hourly_org = (persona.scratch.f_daily_schedule[:])
  
  (created, expiration,
  s, p, o, 
  thought, keywords, 
  thought_poignancy, thought_embedding_pair) = generate_thought_plan(persona, model)
  persona.a_mem.add_thought(created, expiration, s, p, o, 
                            thought, keywords, thought_poignancy, 
                            thought_embedding_pair, None)

def generate_wake_up_hour(persona, model):
  return int(run_prompt_wake_up(persona, model)[0])

def generate_first_daily_plan(persona, wake_up_hour): 
  return run_prompt_daily_plan(persona, wake_up_hour)[0]

def revise_identity(persona, model:LLM_API): 
  p_name = persona.scratch.name
  focal_points = [f"{p_name}'s plan for {persona.scratch.get_str_curr_date_str()}.",
                  f"Important recent events for {p_name}'s life."]

  retrieved = new_retrieve(persona, focal_points)
  _, _, new_currently, new_daily_req = run_prompt_revise_identity(persona, model, retrieved)

  persona.scratch.currently = new_currently
  persona.scratch.daily_plan_req = new_daily_req

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


if __name__ == "__main__":
  from LLM_Character.llm_comms.llm_local import LocalComms
  person = Persona("BANDER")
  modelc = LocalComms()
  model_id = "mistralai/Mistral-7B-Instruct-v0.2"
  modelc.init(model_id)

  model = LLM_API(modelc) 
  _long_term_planning(person, "First day",model)

