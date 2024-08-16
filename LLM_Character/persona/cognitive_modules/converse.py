import sys
sys.path.append('../../../')

from LLM_Character.llm_api import LLM_API 
from LLM_Character.messages_dataclass import AIMessages

from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch 

from LLM_Character.persona.cognitive_modules.conversing.reacting import _generate_response 
from LLM_Character.persona.cognitive_modules.conversing.ending import _end_conversation 

from LLM_Character.persona.prompt_modules.converse_prompts.poignancy_chat import run_prompt_poignancy_chat

def chatting(user_scratch: UserScratch , 
             character_scratch:PersonaScratch, 
             character_mem:AssociativeMemory, 
             message:str,  
             model:LLM_API):

  user_scratch.chat.add_message(message, user_scratch.name, "user", "MessageAI")
  utt, end = _generate_response(user_scratch, character_scratch, character_mem, message, model)
  user_scratch.chat.add_message(utt, character_scratch.name, "assistant", "MessageAI")

  if end:
    _end_conversation(user_scratch, character_scratch, model)   
    p_event = character_scratch.get_curr_event_and_desc()
    _remember_chat(character_scratch, character_mem, p_event, model)
    user_scratch.chat = AIMessages()
  return utt


def _remember_chat(cscratch: PersonaScratch, ca_mem:AssociativeMemory, p_event, model:LLM_API):
  s, p, o, desc = p_event
  desc = f"{s.split(':')[-1]} is {desc}"
  p_event = (s, p, o)

  keywords = set()
  sub = p_event[0]
  obj = p_event[2]
  if ":" in p_event[0]: 
    sub = p_event[0].split(":")[-1]
  if ":" in p_event[2]: 
    obj = p_event[2].split(":")[-1]
  keywords.update([sub, obj])

  if p_event[0] == f"{cscratch.name}" and p_event[1] == "chat with": 
    curr_event = cscratch.act_event

    if cscratch.act_description in ca_mem.embeddings: 
      chat_embedding = ca_mem.embeddings[cscratch.act_description]
    else: 
      chat_embedding = model.get_embedding(cscratch.act_description)

    chat_embedding_pair = (cscratch.act_description, chat_embedding)
    chat_poignancy = generate_poig_score(cscratch, model)
    ca_mem.add_chat(cscratch.curr_time, 
                    None,
                    curr_event[0], 
                    curr_event[1], 
                    curr_event[2], 
                    cscratch.act_description, 
                    keywords, 
                    chat_poignancy, 
                    chat_embedding_pair, 
                    cscratch.chat)

def generate_poig_score(scratch:PersonaScratch, model: LLM_API) : 
    return run_prompt_poignancy_chat(scratch, scratch.act_description, model)[0]


if __name__ == "__main__":
  from LLM_Character.persona.persona import Persona
  from LLM_Character.persona.user import User 
  from LLM_Character.llm_comms.llm_local import LocalComms
  
  print("starting take off ...")
  
  person = Persona("Camila", "../../storage/initial/personas/Camila")
  user = User("Louis", "../../storage/initial/users/Louis")
  modelc = LocalComms()
  
  model_id = "mistralai/Mistral-7B-Instruct-v0.2"
  modelc.init(model_id)

  model = LLM_API(modelc)
  message = "hi"
  response = chatting(user.scratch, person.scratch, person.a_mem, message, model)
  message = "IM TERRIBLE, dont talk to me pls"
  response = chatting(user.scratch, person.scratch, person.a_mem, message, model)
  message = "i said stop talking, end this conversation, bye."
  response = chatting(user.scratch, person.scratch, person.a_mem, message, model)

