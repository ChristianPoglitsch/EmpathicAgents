import datetime
from LLM_Character.persona.cognitive_modules.retrieve import EventContext
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch


def _should_react(persona, focused_event:EventContext, personas): 
  # If the persona is chatting right now, default to no reaction 
  if persona.scratch.chatting_with: 
    return False
  if "<waiting>" in persona.scratch.act_address: # FIXME: where added in the project? 
    return False

  curr_event = focused_event.curr_event
  # this is a persona event if 
  if ":" not in curr_event.subject: 
    if lets_talk(persona, personas[curr_event.subject], focused_event):
      return f"chat with {curr_event.subject}"
    
    react_mode = lets_react(persona, personas[curr_event.subject], focused_event)
    return react_mode
  
  return False

def lets_talk(init_persona_scratch:PersonaScratch, target_persona_scratch:PersonaScratch, retrieved) -> bool:
  # you cant talk if you were doing something. 
  if (not target_persona_scratch.act_address 
      or not target_persona_scratch.act_description
      or not init_persona_scratch.act_address
      or not init_persona_scratch.act_description): 
    return False

  if ("sleeping" in target_persona_scratch.act_description 
      or "sleeping" in init_persona_scratch.act_description): 
    return False

  if init_persona_scratch.curr_time.hour == 23: 
    return False

  if "<waiting>" in target_persona_scratch.act_address: 
    return False

  if (target_persona_scratch.chatting_with 
    or init_persona_scratch.chatting_with): 
    return False

  if (target_persona_scratch.name in init_persona_scratch.chatting_with_buffer): 
    if init_persona_scratch.chatting_with_buffer[target_persona_scratch.name] > 0: 
      return False

  if generate_decide_to_talk(init_persona, target_persona, retrieved): 
    return True
  return False

def lets_react(init_persona, target_persona, retrieved): 
  if (not target_persona.scratch.act_address 
      or not target_persona.scratch.act_description
      or not init_persona.scratch.act_address
      or not init_persona.scratch.act_description): 
    return False

  if ("sleeping" in target_persona.scratch.act_description 
      or "sleeping" in init_persona.scratch.act_description): 
    return False

  if init_persona.scratch.curr_time.hour == 23: 
    return False

  if "waiting" in target_persona.scratch.act_description: 
    return False

  # if init_persona.scratch.planned_path == []:
  #   return False

  if (init_persona.scratch.act_address 
      != target_persona.scratch.act_address): 
    return False

  react_mode = generate_decide_to_react(init_persona, target_persona, retrieved)

  if react_mode == "1": 
    wait_until = ((target_persona.scratch.act_start_time 
      + datetime.timedelta(minutes=target_persona.scratch.act_duration - 1))
      .strftime("%B %d, %Y, %H:%M:%S"))
    return f"wait: {wait_until}"
  return False 
