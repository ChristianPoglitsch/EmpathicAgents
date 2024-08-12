import datetime
import sys
sys.path.append('../../')
from LLM_Character.llm_api import LLM_API 
from LLM_Character.persona.cognitive_modules.planning.long_term_planning import _long_term_planning 
from LLM_Character.persona.cognitive_modules.planning.determine_action import _determine_action 

# FIXME: eerst conversation fixen en dan reflection, reflection laatste.

def reflect(persona):
  if reflection_trigger(persona): 
    run_reflect(persona)
    reset_reflection_counter(persona)

  if persona.scratch.chatting_end_time: 
    if persona.scratch.curr_time + datetime.timedelta(0,10) == persona.scratch.chatting_end_time: 
      all_utt = ""
      if persona.scratch.chat: 
        for row in persona.scratch.chat:  
          all_utt += f"{row[0]}: {row[1]}\n"

      evidence = [persona.a_mem.get_last_chat(persona.scratch.chatting_with).node_id]

      planning_thought = generate_planning_thought_on_convo(persona, all_utt)
      planning_thought = f"For {persona.scratch.name}'s planning: {planning_thought}"

      created = persona.scratch.curr_time
      expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
      s, p, o = generate_action_event_triple(planning_thought, persona)
      keywords = set([s, p, o])
      thought_poignancy = generate_poig_score(persona, "thought", planning_thought)
      thought_embedding_pair = (planning_thought, get_embedding(planning_thought))

      persona.a_mem.add_thought(created, expiration, s, p, o, 
                                planning_thought, keywords, thought_poignancy, 
                                thought_embedding_pair, evidence)


      # FIXME: also important, but why not include iss in
      # prompt or something about persona? 
      memo_thought = generate_memo_on_convo(persona, all_utt)
      memo_thought = f"{persona.scratch.name} {memo_thought}"

      created = persona.scratch.curr_time
      expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
      s, p, o = generate_action_event_triple(memo_thought, persona)
      keywords = set([s, p, o])
      thought_poignancy = generate_poig_score(persona, "thought", memo_thought)
      thought_embedding_pair = (memo_thought, get_embedding(memo_thought))

      persona.a_mem.add_thought(created, expiration, s, p, o, 
                                memo_thought, keywords, thought_poignancy, 
                                thought_embedding_pair, evidence)



def reflection_trigger(persona): 
  print (persona.scratch.name, "persona.scratch.importance_trigger_curr::", persona.scratch.importance_trigger_curr)
  print (persona.scratch.importance_trigger_max)

  if (persona.scratch.importance_trigger_curr <= 0 and 
      [] != persona.a_mem.seq_event + persona.a_mem.seq_thought): 
    return True 
  return False


def run_reflect(persona):
  # Reflection requires certain focal points. Generate that first. 
  focal_points = generate_focal_points(persona, 3)
  # Retrieve the relevant Nodes object for each of the focal points. 
  # <retrieved> has keys of focal points, and values of the associated Nodes. 
  retrieved = retrieve(persona, focal_points)

  # For each of the focal points, generate thoughts and save it in the 
  # agent's memory. 
  for focal_pt, nodes in retrieved.items(): 
    xx = [i.embedding_key for i in nodes]
    for xxx in xx: print (xxx)

    thoughts = generate_insights_and_evidence(persona, nodes, 5)
    for thought, evidence in thoughts.items(): 
      created = persona.scratch.curr_time
      expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
      s, p, o = generate_action_event_triple(thought, persona)
      keywords = set([s, p, o])
      thought_poignancy = generate_poig_score(persona, "thought", thought)
      thought_embedding_pair = (thought, get_embedding(thought))

      persona.a_mem.add_thought(created, expiration, s, p, o, 
                                thought, keywords, thought_poignancy, 
                                thought_embedding_pair, evidence)


def reset_reflection_counter(persona): 
  persona_imt_max = persona.scratch.importance_trigger_max
  persona.scratch.importance_trigger_curr = persona_imt_max
  persona.scratch.importance_ele_n = 0

def generate_planning_thought_on_convo(persona, all_utt):
  return run_prompt_planning_thought_on_convo(persona, all_utt)[0]


def generate_poig_score(persona, event_type, description): 
  if "is idle" in description: 
    return 1

  if event_type == "event" or event_type == "thought": 
    return run_prompt_event_poignancy(persona, description)[0]
  elif event_type == "chat": 
    return run_prompt_chat_poignancy(persona, 
                           persona.scratch.act_description)[0]

def generate_memo_on_convo(persona, all_utt):
  return run_prompt_memo_on_convo(persona, all_utt)[0]

def generate_action_event_triple(act_desp, persona): 
  return run_prompt_event_triple(act_desp, persona)[0]

if __name__ == "__main__":
  from LLM_Character.persona.persona import Persona
  from llm_comms.llm_local import LocalComms
  person = Persona("MIKE")
  modelc = LocalComms()
  
  model_id = "mistralai/Mistral-7B-Instruct-v0.2"
  modelc.init(model_id)

  model = LLM_API(modelc)
  reflect(person, model)
