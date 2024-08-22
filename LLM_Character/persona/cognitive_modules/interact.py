from LLM_Character.llm_comms.llm_api import LLM_API 

from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch 
from LLM_Character.persona.cognitive_modules.retrieve import retrieve_contextual_events



def interact(retrieved, scratch:PersonaScratch, personas:dict[str, PersonaScratch]):
  # focused_event = False
  # if retrieved.keys(): 
  #   focused_event = _choose_retrieved(scratch, retrieved)
  
  # if focused_event: 
  #   reaction_mode = _should_react(scratch, focused_event, personas)
  #   if reaction_mode: 
  #     if reaction_mode[:9] == "chat with":
  #       _chat_react(scratch, focused_event, reaction_mode, personas)
  #     elif reaction_mode[:4] == "wait": 
  #       _wait_react(scratch, reaction_mode)

  # if scratch.act_event[1] != "chat with":
  #   scratch.chatting_with = None
  #   scratch.chat = None
  #   scratch.chatting_end_time = None
  
  # curr_persona_chat_buffer = scratch.chatting_with_buffer
  # for persona_name, buffer_count in curr_persona_chat_buffer.items():
  #   if persona_name != scratch.chatting_with: 
  #     scratch.chatting_with_buffer[persona_name] -= 1

  # return scratch.act_address
  return None