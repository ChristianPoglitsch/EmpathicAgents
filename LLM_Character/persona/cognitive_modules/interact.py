import datetime
import random

from LLM_Character.llm_comms.llm_api import LLM_API 
from LLM_Character.persona.cognitive_modules.retrieve import EventContext
from LLM_Character.persona.cognitive_modules.conversing.ending import _create_react 
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch

from LLM_Character.persona.cognitive_modules.interacting.reacting import _should_react
from LLM_Character.persona.cognitive_modules.interacting.chatting import _chat_react


def interact(scratch:PersonaScratch, personas:dict[str, PersonaScratch], retrieved: dict[str, EventContext], model:LLM_API):
  focused_event = False
  if retrieved.keys(): 
    focused_event = _choose_retrieved(scratch, retrieved)
  
  if focused_event: 
    reaction_mode = _should_react(scratch, focused_event, personas)
    if reaction_mode: 
      if reaction_mode[:9] == "chat with":
        _chat_react(scratch, reaction_mode, personas)
      elif reaction_mode[:4] == "wait": 
        _wait_react(scratch, reaction_mode)

  if scratch.act_event[1] != "chat with":
    scratch.chatting_with = None
    scratch.chat = None
    scratch.chatting_end_time = None
  
  curr_persona_chat_buffer = scratch.chatting_with_buffer
  for persona_name, buffer_count in curr_persona_chat_buffer.items():
    if persona_name != scratch.chatting_with: 
      scratch.chatting_with_buffer[persona_name] -= 1

  return scratch.act_address

def _choose_retrieved(cscratch:PersonaScratch, retrieved: dict[str, EventContext]) -> EventContext: 
  # dont think we need this, since self events are not sent?
  # but still could be left here: 
  copy_retrieved = retrieved.copy()
  for event_desc, rel_ctx in copy_retrieved.items(): 
    curr_event = rel_ctx.curr_event
    if curr_event.subject == cscratch.name: 
      del retrieved[event_desc]

  # Always choose persona first.
  priority = []
  for event_desc, rel_ctx in retrieved.items(): 
    curr_event = rel_ctx.curr_event
    if (":" not in curr_event.subject 
        and curr_event.subject != cscratch.name): 
      priority += [rel_ctx]
  if priority: 
    return random.choice(priority)

  # Skip idle. 
  for event_desc, rel_ctx in retrieved.items(): 
    curr_event = rel_ctx.curr_event
    if "is idle" not in event_desc: 
      priority += [rel_ctx]
  if priority: 
    return random.choice(priority)
  return None

def _wait_react(persona, reaction_mode): 
  p = persona

  inserted_act = f'waiting to start {p.scratch.act_description.split("(")[-1][:-1]}'
  end_time = datetime.datetime.strptime(reaction_mode[6:].strip(), "%B %d, %Y, %H:%M:%S")
  inserted_act_dur = (end_time.minute + end_time.hour * 60) - (p.scratch.curr_time.minute + p.scratch.curr_time.hour * 60) + 1

  act_address = f"<waiting> {p.scratch.curr_tile[0]} {p.scratch.curr_tile[1]}"
  act_event = (p.name, "waiting to start", p.scratch.act_description.split("(")[-1][:-1])
  chatting_with = None
  chat = None
  chatting_with_buffer = None
  chatting_end_time = None

  act_obj_description = None
  act_obj_pronunciatio = None
  act_obj_event = (None, None, None)

  _create_react(p, inserted_act, inserted_act_dur,
    act_address, act_event, chatting_with, chat, chatting_with_buffer, chatting_end_time,
    act_obj_description, act_obj_pronunciatio, act_obj_event)
