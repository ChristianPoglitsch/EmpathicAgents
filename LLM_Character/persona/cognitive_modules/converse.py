import datetime
import sys
sys.path.append('../../')

from LLM_Character.llm_api import LLM_API 

from LLM_Character.persona.cognitive_modules.retrieve import retrieve 
from LLM_Character.persona.prompt_modules.converse_prompts.summarize_ideas import run_prompt_summarize_ideas
from LLM_Character.persona.prompt_modules.converse_prompts.generate_line import run_prompt_generate_next_conv_line
from LLM_Character.messages_dataclass import AIMessages

# FIXME no need for curr_convo, you should extract that from memory. 
# personas.scratch.chat should be AIMessages.

# FIXME interlocutor_desc should be 'unkown' first. 
# then querry LLM and see if they know who 
# they are by qeurying their previous conversation
# and extracting the necessary information. 

# NOTE too naive
# retrieved = retrieve(persona, [message], model, 50)[message]
# summarized_idea = generate_summarize_ideas(persona, retrieved, message)
#
# next_line = generate_next_line(persona, curr_convo, summarized_idea)

# TODO add chat to memory
# curr_convo.add_message_role(message, "user")
# curr_convo.add_message_role(next_line, persona.scratch.name)

def open_convo_session(user_persona, character_persona, message:str,  model:LLM_API): 

  # generate_convo(maze, init_persona, target_persona)
  curr_loc = user_persona.scratch.curr_location
  curr_chat = user_persona.scratch.chatting_buffer
  focal_points = [f"{character_persona.scratch.name}"]
  retrieved = retrieve(user_persona, focal_points, model, 50)
  relationship = generate_summarize_agent_relationship(user_persona, character_persona, retrieved)
  
  last_chat = ""
  for i in curr_chat[-4:]:
    last_chat += ": ".join(i) + "\n"

  if last_chat: 
    focal_points = [f"{relationship}", 
                    f"{character_persona.scratch.name} is {character_persona.scratch.act_description}", last_chat]
  else: 
    focal_points = [f"{relationship}", 
                    f"{character_persona.scratch.name} is {character_persona.scratch.act_description}"]


def agent_chat(init_persona, target_persona): 
  curr_chat = []
  print ("July 23")

  for i in range(8): 
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}"]
    retrieved = new_retrieve(init_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, init_persona, target_persona, retrieved, curr_chat)

    curr_chat += [[init_persona.scratch.name, utt]]
    if end:
      break


    focal_points = [f"{init_persona.scratch.name}"]
    retrieved = new_retrieve(target_persona, focal_points, 50)
    relationship = generate_summarize_agent_relationship(target_persona, init_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}"]
    retrieved = new_retrieve(target_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, target_persona, init_persona, retrieved, curr_chat)

    curr_chat += [[target_persona.scratch.name, utt]]
    if end:
      break

  print ("July 23 PU")
  for row in curr_chat: 
    print (row)
  print ("July 23 FIN")

  return curr_chat












def generate_summarize_ideas(persona, nodes, question): 
  statements = ""
  for n in nodes:
    statements += f"{n.embedding_key}\n"
  summarized_idea = run_prompt_summarize_ideas(persona, statements, question)[0]
  return summarized_idea

def generate_next_line(persona, curr_convo:AIMessages, summarized_idea):
  str_convo = curr_convo.prints_messages()
  # TODO maybe need to reformat this
  # str_convo.replace("[assistant"]", f"{persona.scratch.name}:")
  # str_convo.replace("[user]", "interviewer:")
  next_line = run_prompt_generate_next_conv_line(persona, interlocutor_desc, str_convo, summarized_idea)[0]  
  return next_line


def chat(maze, persona, focused_event, reaction_mode, personas):
  init_persona = persona
  target_persona = personas[reaction_mode[9:].strip()]
  
  convo, duration_min = generate_convo(maze, init_persona, target_persona)
  convo_summary = generate_convo_summary(init_persona, convo)
  
  inserted_act = convo_summary
  inserted_act_dur = duration_min

  act_address = f"<persona> {target_persona.name}"
  act_event = (p.name, "chat with", target_persona.name)
  chatting_with = target_persona.name
  chatting_with_buffer = {}
  chatting_with_buffer[target_persona.name] = 800

  act_pronunciatio = "💬" 
  act_obj_description = None
  act_obj_pronunciatio = None
  act_obj_event = (None, None, None)

  _create_react(persona, inserted_act, inserted_act_dur,
    act_address, act_event, chatting_with, convo, chatting_with_buffer, chatting_end_time,
    act_pronunciatio, act_obj_description, act_obj_pronunciatio, 
    act_obj_event, act_start_time)



def generate_convo(maze, init_persona, target_persona): 
  curr_loc = maze.access_tile(init_persona.scratch.curr_tile)

  # convo = run_gpt_prompt_create_conversation(init_persona, target_persona, curr_loc)[0]
  # convo = agent_chat_v1(maze, init_persona, target_persona)
  convo = agent_chat_v2(maze, init_persona, target_persona)
  all_utt = ""

  for row in convo: 
    speaker = row[0]
    utt = row[1]
    all_utt += f"{speaker}: {utt}\n"

  convo_length = math.ceil(int(len(all_utt)/8) / 30)

  if debug: print ("GNS FUNCTION: <generate_convo>")
  return convo, convo_length


def generate_convo_summary(persona, convo): 
  convo_summary = run_gpt_prompt_summarize_conversation(persona, convo)[0]
  return convo_summary


def _create_react(persona, inserted_act, inserted_act_dur,
                  act_address, act_event, chatting_with, chat, chatting_with_buffer,
                  chatting_end_time, 
                  act_pronunciatio, act_obj_description, act_obj_pronunciatio, 
                  act_obj_event, act_start_time=None): 
  p = persona 

  min_sum = 0
  for i in range (p.scratch.get_f_daily_schedule_hourly_org_index()): 
    min_sum += p.scratch.f_daily_schedule_hourly_org[i][1]
  start_hour = int (min_sum/60)

  if (p.scratch.f_daily_schedule_hourly_org[p.scratch.get_f_daily_schedule_hourly_org_index()][1] >= 120):
    end_hour = start_hour + p.scratch.f_daily_schedule_hourly_org[p.scratch.get_f_daily_schedule_hourly_org_index()][1]/60

  elif (p.scratch.f_daily_schedule_hourly_org[p.scratch.get_f_daily_schedule_hourly_org_index()][1] + 
      p.scratch.f_daily_schedule_hourly_org[p.scratch.get_f_daily_schedule_hourly_org_index()+1][1]): 
    end_hour = start_hour + ((p.scratch.f_daily_schedule_hourly_org[p.scratch.get_f_daily_schedule_hourly_org_index()][1] + 
              p.scratch.f_daily_schedule_hourly_org[p.scratch.get_f_daily_schedule_hourly_org_index()+1][1])/60)

  else: 
    end_hour = start_hour + 2
  end_hour = int(end_hour)

  dur_sum = 0
  count = 0 
  start_index = None
  end_index = None
  for act, dur in p.scratch.f_daily_schedule: 
    if dur_sum >= start_hour * 60 and start_index == None:
      start_index = count
    if dur_sum >= end_hour * 60 and end_index == None: 
      end_index = count
    dur_sum += dur
    count += 1

  ret = generate_new_decomp_schedule(p, inserted_act, inserted_act_dur, 
                                       start_hour, end_hour)
  p.scratch.f_daily_schedule[start_index:end_index] = ret
  p.scratch.add_new_action(act_address,
                           inserted_act_dur,
                           inserted_act,
                           act_pronunciatio,
                           act_event,
                           chatting_with,
                           chat,
                           chatting_with_buffer,
                           chatting_end_time,
                           act_obj_description,
                           act_obj_pronunciatio,
                           act_obj_event,
                           act_start_time)



def agent_chat(init_persona, target_persona): 
  curr_chat = []
  print ("July 23")

  for i in range(8): 
    focal_points = [f"{target_persona.scratch.name}"]
    retrieved = new_retrieve(init_persona, focal_points, 50)
    relationship = generate_summarize_agent_relationship(init_persona, target_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}"]
    retrieved = new_retrieve(init_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, init_persona, target_persona, retrieved, curr_chat)

    curr_chat += [[init_persona.scratch.name, utt]]
    if end:
      break


    focal_points = [f"{init_persona.scratch.name}"]
    retrieved = new_retrieve(target_persona, focal_points, 50)
    relationship = generate_summarize_agent_relationship(target_persona, init_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}"]
    retrieved = new_retrieve(target_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, target_persona, init_persona, retrieved, curr_chat)

    curr_chat += [[target_persona.scratch.name, utt]]
    if end:
      break

  print ("July 23 PU")
  for row in curr_chat: 
    print (row)
  print ("July 23 FIN")

  return curr_chat

