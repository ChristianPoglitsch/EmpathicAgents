import datetime
import sys
import math
sys.path.append('../../')

from LLM_Character.llm_api import LLM_API 

from LLM_Character.persona.prompt_modules.converse_prompts.summarize_relationship import run_prompt_summarize_relationship 
from LLM_Character.persona.prompt_modules.converse_prompts.generate_iterative_chat import run_prompt_iterative_chat 
from LLM_Character.persona.prompt_modules.converse_prompts.summarize_conversation import run_prompt_summarize_conversation
from LLM_Character.persona.prompt_modules.converse_prompts.decomp_schedule import run_prompt_decomp_schedule

from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory,  ConceptNode
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch 

from LLM_Character.persona.cognitive_modules.retrieve import retrieve 
from LLM_Character.messages_dataclass import AIMessages


# FIXME no need for curr_convo, you should extract that from memory. 
# personas.scratch.chat should be AIMessages.

# NOTE too naive
# retrieved = retrieve(persona, [message], model, 50)[message]
# summarized_idea = generate_summarize_ideas(persona, retrieved, message)
#
# next_line = generate_next_line(persona, curr_convo, summarized_idea)

# TODO add chat to memory
# curr_convo.add_message_role(message, "user")
# curr_convo.add_message_role(next_line, persona.scratch.name)


def chatting(user_scratch: UserScratch , character_mem:AssociativeMemory, character_scratch:PersonaScratch, message:str,  model:LLM_API) : 
  # TODO add message to curr_chat ? or to scratch.chat probably better.

  # TODO mogelijke verbetering: aadd message as focal point 
  # retrieved = retrieve(persona, [message], model, 50)[message]
  # hieronder wordt enkel informatie over degene die de message heeft gesuurd retrieved, maar er wordt
  # niets gertrieved over de message zelf zoals hierboven.

  focal_points = [f"{user_scratch.name}"]
  retrieved = retrieve(character_scratch, character_mem, focal_points, model, 50)
  relationship = generate_summarize_agent_relationship(user_scratch, character_scratch, model, retrieved)
  
  # FIXME vervang curr_chat met scratch.chat? and scratch.chat in AI_Messages opgeslagen?  
  curr_chat = [] 
  last_chat = ""
  for i in curr_chat[-4:]:
    last_chat += ": ".join(i) + "\n"
  
  if last_chat: 
    focal_points = [f"{relationship}", 
                    f"{character_scratch.name} is {character_scratch.act_description}", 
                    last_chat]
  else: 
    focal_points = [f"{relationship}", 
                    f"{character_scratch.name} is {character_scratch.act_description}"]
  
  retrieved = retrieve(user_scratch, character_mem, focal_points, model, 15)
  utt, end = generate_one_utterance(user_scratch, character_mem, character_scratch, model, retrieved, curr_chat)


  curr_chat += [[character_scratch.name, utt]]
  

  if end: 
    convo_summary = generate_convo_summary(init_persona, convo)

    all_utt = ""
    for row in curr_chat: 
      speaker = row[0]
      utt = row[1]
      all_utt += f"{speaker}: {utt}\n"

    convo_length = math.ceil(int(len(all_utt)/8) / 30)
  
    inserted_act = convo_summary
    inserted_act_dur = duration_min

    act_address = f"<persona> {character_scratch.name}"
    act_event = (user_scratch.name, "chat with", character_scratch.name)
    chatting_with = character_scratch.name
    chatting_with_buffer = {}
    chatting_with_buffer[character_scratch.name] = 800

    _create_react(character_scratch, 
                  inserted_act, 
                  inserted_act_dur,
                  act_address, 
                  act_event, 
                  chatting_with, 
                  curr_chat, 
                  chatting_with_buffer, 
                  chatting_end_time, 
                  act_start_time)

    # FIXME: add this event to memory stream
    # add chat to memory stream.

    # if end:
    # TODO empty curr_chat or scratch.chat
      # return end_chat, send message to unity to disable chat modus for example. 
    return curr_chat, convo_length
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
                           uamem: AssociativeMemory,
                           cscratch:PersonaScratch,
                           model: LLM_API, 
                           retrieved:dict[str, list[ConceptNode]],
                           curr_chat,
                           ):
  curr_context = (f"{uscratch.name} " + 
              f"was {uscratch.act_description} " + 
              f"when {uscratch.name} " + 
              f"saw {cscratch.name} " + 
              f"in the middle of {cscratch.act_description}.\n")
  curr_context += (f"{uscratch.name} " +
              f"is initiating a conversation with " +
              f"{cscratch.name}.")
  x = run_prompt_iterative_chat(uscratch, uamem, cscratch, model, retrieved, curr_context, curr_chat)
  #FIXME: if x is not a string..... 
  return x['utterance'], x['end']


def generate_convo_summary(persona, convo): 
  convo_summary = run_prompt_summarize_conversation(persona, convo)[0]
  return convo_summary


def _create_react(cscratch:PersonaScratch, 
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

  ret = generate_new_decomp_schedule(cscratch, inserted_act, inserted_act_dur, 
                                       start_hour, end_hour)
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

def generate_new_decomp_schedule(cscratch, inserted_act, inserted_act_dur,  start_hour, end_hour): 
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
                                    inserted_act_dur)[0]
