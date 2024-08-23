import datetime
import math 

from LLM_Character.persona.cognitive_modules.conversing.ending import generate_convo_summary, _create_react
from LLM_Character.persona.cognitive_modules.retrieve import retrieve_focal_points
from LLM_Character.persona.cognitive_modules.conversing.reacting import run_prompt_iterative_chat
from LLM_Character.persona.cognitive_modules.conversing.reacting import run_prompt_summarize_relationship

def _chat_react(maze, persona, reaction_mode, personas):
  # There are two personas -- the persona who is initiating the conversation
  # and the persona who is the target. We get the persona instances here. 
  init_persona = persona
  target_persona = personas[reaction_mode[9:].strip()]
  curr_personas = [init_persona, target_persona]

  # Actually creating the conversation here. 
  convo, duration_min = generate_convo(maze, init_persona, target_persona)
  convo_summary = generate_convo_summary(init_persona, convo)
  inserted_act = convo_summary
  inserted_act_dur = duration_min

  act_start_time = target_persona.scratch.act_start_time

  curr_time = target_persona.scratch.curr_time
  if curr_time.second != 0: 
    temp_curr_time = curr_time + datetime.timedelta(seconds=60 - curr_time.second)
    chatting_end_time = temp_curr_time + datetime.timedelta(minutes=inserted_act_dur)
  else: 
    chatting_end_time = curr_time + datetime.timedelta(minutes=inserted_act_dur)

  for role, p in [("init", init_persona), ("target", target_persona)]: 
    if role == "init": 
      act_address = f"<persona> {target_persona.name}"
      act_event = (p.name, "chat with", target_persona.name)
      chatting_with = target_persona.name
      chatting_with_buffer = {}
      chatting_with_buffer[target_persona.name] = 800
    
    elif role == "target": 
      act_address = f"<persona> {init_persona.name}"
      act_event = (p.name, "chat with", init_persona.name)
      chatting_with = init_persona.name
      chatting_with_buffer = {}
      chatting_with_buffer[init_persona.name] = 800

    act_obj_description = None
    act_obj_pronunciatio = None
    act_obj_event = (None, None, None)

    _create_react(p, inserted_act, inserted_act_dur,
      act_address, act_event, chatting_with, convo, chatting_with_buffer, chatting_end_time,
      act_obj_description, act_obj_pronunciatio, 
      act_obj_event, act_start_time)

def generate_convo(maze, init_persona, target_persona): 
  convo = agent_chat_v2(maze, init_persona, target_persona)
  all_utt = ""

  for row in convo: 
    speaker = row[0]
    utt = row[1]
    all_utt += f"{speaker}: {utt}\n"

  convo_length = math.ceil(int(len(all_utt)/8) / 30)

  return convo, convo_length

def agent_chat_v2(maze, init_persona, target_persona): 
  curr_chat = []

  for i in range(8): 
    focal_points = [f"{target_persona.scratch.name}"]
    retrieved = retrieve_focal_points(init_persona, focal_points, 50)
    relationship = run_prompt_summarize_relationship(init_persona, target_persona, retrieved)
    
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
    retrieved = retrieve_focal_points(init_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, init_persona, target_persona, retrieved, curr_chat)

    curr_chat += [[init_persona.scratch.name, utt]]
    if end:
      break

    focal_points = [f"{init_persona.scratch.name}"]
    retrieved = retrieve_focal_points(target_persona, focal_points, 50)
    relationship = run_prompt_summarize_relationship(target_persona, init_persona, retrieved)
    
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
    retrieved = retrieve_focal_points(target_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, target_persona, init_persona, retrieved, curr_chat)

    curr_chat += [[target_persona.scratch.name, utt]]
    if end:
      break
  
  return curr_chat


def generate_one_utterance(maze, init_persona, target_persona, retrieved, curr_chat): 
  # Chat version optimized for speed via batch generation
  curr_context = (f"{init_persona.scratch.name} " + 
              f"was {init_persona.scratch.act_description} " + 
              f"when {init_persona.scratch.name} " + 
              f"saw {target_persona.scratch.name} " + 
              f"in the middle of {target_persona.scratch.act_description}.\n")
  curr_context += (f"{init_persona.scratch.name} " +
              f"is initiating a conversation with " +
              f"{target_persona.scratch.name}.")

  x = run_prompt_iterative_chat(maze, init_persona, target_persona, retrieved, curr_context, curr_chat)[0]

  return x["utterance"], x["end"]
