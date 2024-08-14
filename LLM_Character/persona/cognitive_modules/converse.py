import datetime
import sys
import math
sys.path.append('../../')

from LLM_Character.llm_api import LLM_API 

from LLM_Character.persona.prompt_modules.converse_prompts.summarize_relationship import run_prompt_summarize_relationship 
from LLM_Character.persona.prompt_modules.converse_prompts.generate_iterative_chat import run_prompt_iterative_chat 
from LLM_Character.persona.prompt_modules.converse_prompts.summarize_conversation import run_prompt_summarize_conversation
from LLM_Character.persona.prompt_modules.converse_prompts.decomp_schedule import run_prompt_decomp_schedule
from LLM_Character.persona.prompt_modules.converse_prompts.poignancy_chat import run_prompt_poignancy_chat

from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory,  ConceptNode
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch 

from LLM_Character.persona.cognitive_modules.retrieve import retrieve 
from LLM_Character.persona.cognitive_modules.reflect import reflect 
from LLM_Character.messages_dataclass import AIMessage, AIMessages


def chatting(user_scratch: UserScratch , 
             character_scratch:PersonaScratch, 
             character_mem:AssociativeMemory, 
             message:str,  
             model:LLM_API):

  # YOU WANT TO CREATE A MESSAGE DIRECTED TO USER! 
  focal_points = [f"{user_scratch.name}"]
  retrieved = retrieve(character_scratch, character_mem, focal_points, model, 50)
  relationship = generate_summarize_agent_relationship(user_scratch, character_scratch, model, retrieved)
 
  curr_chat = user_scratch.chat.get_messages() 
  last_chat = ""
  for i in curr_chat[-4:]:
    last_chat += i.print_message_sender()
  
  if last_chat: 
    focal_points = [f"{relationship}", 
                    f"{character_scratch.name} is {character_scratch.act_description}", 
                    last_chat]
  else: 
    focal_points = [f"{relationship}", 
                    f"{character_scratch.name} is {character_scratch.act_description}"]
  
  # NOTE add message as focal point 
  focal_points = [f"{user_scratch.name}", message]
  retrieved = retrieve(character_scratch, character_mem, focal_points, model, 15)
  utt, end = generate_one_utterance(user_scratch, 
                                    character_scratch, 
                                    character_mem, 
                                    model, 
                                    retrieved, 
                                    curr_chat[-8:])

  user_scratch.chat.add_message(message, user_scratch.name, "User", "MessageAI")
  user_scratch.chat.add_message(utt, character_scratch.name, "Assistant", "MessageAI") 
  
  if end:
    user_scratch.chat = AIMessages()

    convo_summary = generate_convo_summary(init_persona, convo)
    last_chat = ""
    for i in curr_chat:
      last_chat += i.print_message_sender()
  
    inserted_act = convo_summary
    inserted_act_dur = math.ceil(int(len(last_chat)/8) / 30) 
    
    
    act_address = f"<persona> {user_scratch.name}"
    act_event = (character_scratch.name, "chat with", user_scratch.name)
    chatting_with = user_scratch.name
    chatting_with_buffer = {}
    chatting_with_buffer[user_scratch.name] = 800
    
    curr_time = character_scratch.curr_time
    if curr_time.second != 0: 
      temp_curr_time = curr_time + datetime.timedelta(seconds=60 - curr_time.second)
      chatting_end_time = temp_curr_time + datetime.timedelta(minutes=inserted_act_dur)
    else: 
      chatting_end_time = curr_time + datetime.timedelta(minutes=inserted_act_dur)
    
    act_start_time = character_scratch.act_start_time # FIXME not sure
    
    _create_react(character_scratch, 
                  model,
                  inserted_act, 
                  inserted_act_dur,
                  act_address, 
                  act_event, 
                  chatting_with, 
                  curr_chat, 
                  chatting_with_buffer, 
                  chatting_end_time, 
                  act_start_time)
    
    p_event = reflect(character_scratch, character_mem)
    remember_chat(character_scratch, character_mem, p_event, model)
  return utt
  
def generate_summarize_agent_relationship(user_scratch: UserScratch , 
                                          character_scratch:PersonaScratch,
                                          model: LLM_API, 
                                          retrieved:dict[str, list[ConceptNode]]):
  all_embedding_keys = list()
  for _, val in retrieved.items(): 
    for i in val: 
      all_embedding_keys += [i.embedding_key]
  all_embedding_key_str =""
  for i in all_embedding_keys: 
    all_embedding_key_str += f"{i}\n"

  summarized_relationship = run_prompt_summarize_relationship(
                              user_scratch,
                              character_scratch,
                              model,
                              all_embedding_key_str)[0]
  return summarized_relationship

def generate_one_utterance(uscratch: UserScratch,
                           cscratch:PersonaScratch,
                           camem: AssociativeMemory,
                           model: LLM_API, 
                           retrieved:dict[str, list[ConceptNode]],
                           curr_chat:list[AIMessage]):
  # FIXME dont know if this context will always work, check later when everything is in place. 
  curr_context = (f"{cscratch.name} " + 
              f"was {cscratch.act_description} " + 
              f"when {cscratch.name} " + 
              f"saw {uscratch.name} " + 
              f"in the middle of {uscratch.act_description}.\n")
  curr_context += (f"{cscratch.name} " +
              f"is initiating a conversation with " +
              f"{uscratch.name}.")
  x = run_prompt_iterative_chat(uscratch, cscratch, camem, model, retrieved, curr_context, curr_chat)
  return x['utterance'], x['end']


def generate_convo_summary(persona, convo): 
  convo_summary = run_prompt_summarize_conversation(persona, convo)[0]
  return convo_summary


def _create_react(cscratch:PersonaScratch,
                  model:LLM_API,
                  inserted_act, 
                  inserted_act_dur,
                  act_address, 
                  act_event, 
                  chatting_with, 
                  chat, 
                  chatting_with_buffer,
                  chatting_end_time, 
                  act_start_time=None): 

  min_sum = 0
  for i in range (cscratch.get_f_daily_schedule_hourly_org_index()): 
    min_sum += cscratch.f_daily_schedule_hourly_org[i][1]
  start_hour = int (min_sum/60)

  if (cscratch.f_daily_schedule_hourly_org[cscratch.get_f_daily_schedule_hourly_org_index()][1] >= 120):
    end_hour = start_hour + cscratch.f_daily_schedule_hourly_org[cscratch.get_f_daily_schedule_hourly_org_index()][1]/60

  elif (cscratch.f_daily_schedule_hourly_org[cscratch.get_f_daily_schedule_hourly_org_index()][1] + 
      cscratch.f_daily_schedule_hourly_org[cscratch.get_f_daily_schedule_hourly_org_index()+1][1]): 
    end_hour = start_hour + ((cscratch.f_daily_schedule_hourly_org[cscratch.get_f_daily_schedule_hourly_org_index()][1] + 
              cscratch.f_daily_schedule_hourly_org[cscratch.get_f_daily_schedule_hourly_org_index()+1][1])/60)

  else: 
    end_hour = start_hour + 2
  end_hour = int(end_hour)

  dur_sum = 0
  count = 0 
  start_index = None
  end_index = None
  for act, dur in cscratch.f_daily_schedule: 
    if dur_sum >= start_hour * 60 and start_index == None:
      start_index = count
    if dur_sum >= end_hour * 60 and end_index == None: 
      end_index = count
    dur_sum += dur
    count += 1

  ret = generate_new_decomp_schedule(cscratch,
                                     model,
                                     inserted_act, 
                                     inserted_act_dur, 
                                     start_hour, 
                                     end_hour)
  cscratch.f_daily_schedule[start_index:end_index] = ret
  cscratch.add_new_action(act_address,
                           inserted_act_dur,
                           inserted_act,
                           act_event,
                           chatting_with,
                           chat,
                           chatting_with_buffer,
                           chatting_end_time,
                           act_start_time)

def generate_new_decomp_schedule(cscratch, 
                                 model:LLM_API,
                                 inserted_act, 
                                 inserted_act_dur,  
                                 start_hour, 
                                 end_hour): 
  today_min_pass = (int(cscratch.curr_time.hour) * 60 + int(cscratch.curr_time.minute) + 1)
  main_act_dur = []
  truncated_act_dur = []
  dur_sum = 0
  count = 0 
  truncated_fin = False 

  for act, dur in cscratch.f_daily_schedule: 
    if (dur_sum >= start_hour * 60) and (dur_sum < end_hour * 60): 
      main_act_dur += [[act, dur]]
      if dur_sum <= today_min_pass:
        truncated_act_dur += [[act, dur]]
      elif dur_sum > today_min_pass and not truncated_fin: 
        truncated_act_dur += [[cscratch.f_daily_schedule[count][0], dur_sum - today_min_pass]] 
        truncated_act_dur[-1][-1] -= (dur_sum - today_min_pass) 
        truncated_fin = True
    dur_sum += dur
    count += 1

  main_act_dur = main_act_dur
  y = " (on the way to " + truncated_act_dur[-1][0].split("(")[-1][:-1] + ")"
  x = truncated_act_dur[-1][0].split("(")[0].strip() + y
  truncated_act_dur[-1][0] = x 

  if "(" in truncated_act_dur[-1][0]: 
    inserted_act = truncated_act_dur[-1][0].split("(")[0].strip() + " (" + inserted_act + ")"

  truncated_act_dur += [[inserted_act, inserted_act_dur]]
  start_time_hour = (datetime.datetime(2022, 10, 31, 0, 0) 
                   + datetime.timedelta(hours=start_hour))
  end_time_hour = (datetime.datetime(2022, 10, 31, 0, 0) 
                   + datetime.timedelta(hours=end_hour))

  return run_prompt_decomp_schedule(cscratch, 
                                    main_act_dur, 
                                    truncated_act_dur, 
                                    start_time_hour,
                                    end_time_hour,
                                    inserted_act,
                                    inserted_act_dur,
                                    model)[0]


def remember_chat(cscratch: PersonaScratch, ca_mem:AssociativeMemory, p_event, model):
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
    chat_poignancy = generate_poig_score(cscratch)
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

def generate_poig_score(scratch:PersonaScratch) : 
    return run_prompt_poignancy_chat(scratch)[0]
