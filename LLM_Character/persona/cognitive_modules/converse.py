import datetime
import shutil, errno
import json 

def copyanything(src, dst):
  try:
    shutil.copytree(src, dst)
  except OSError as exc: # python >2.5
    if exc.errno in (errno.ENOTDIR, errno.EINVAL):
      shutil.copy(src, dst)
    else: raise



# TODO move this variable to env file. 
FS_STORAGE = "LLM_Chracter/storage"

# TODO initial setup
class ReverieServer:
  def __init__(self,
               fork_sim_code:str,
               sim_code:str):

    self.fork_sim_code = fork_sim_code
    self.sim_code = sim_code

    fork_folder = f"{FS_STORAGE}/{self.fork_sim_code}"
    sim_folder = f"{FS_STORAGE}/{self.sim_code}"

    copyanything(fork_folder, sim_folder)
    with open(f"{sim_folder}/reverie/meta.json") as json_file:  
      reverie_meta = json.load(json_file)

    with open(f"{sim_folder}/reverie/meta.json", "w") as outfile: 
      reverie_meta["fork_sim_code"] = fork_sim_code
      outfile.write(json.dumps(reverie_meta, indent=2))

    self.curr_time = datetime.datetime.strptime(reverie_meta['curr_time'], "%B %d, %Y, %H:%M:%S")
    self.sec_per_step = reverie_meta['sec_per_step']
    self.step = reverie_meta['step']

    self.personas = dict()

    init_env_file = f"{sim_folder}/environment/{str(self.step)}.json"
    init_env = json.load(open(init_env_file))
    for persona_name in reverie_meta['persona_names']: 
      persona_folder = f"{sim_folder}/personas/{persona_name}"
      curr_persona = Persona(persona_name, persona_folder)





# TODO check if line is similar to a sentence
# "end conversation or bye".
# instead of having a hardcoded command.
# see model.semantig_meaning or model.semanting_relationship
def reverie(message:str):

  if message == 'n':
      print("--- reset chat ---")
      messages = messages.read_messages_from_json("dialogues/background.json")
      # TODO reset persona, and delete memory. 
  elif message == 'e':
      print("--- end chat ---")
      # TODO shouldnt need command. 
  else:
      open_convo_session(persona, messages)

      messages, response = model.query(pm._message, messages)




# model asks for name of interviewer, and builds persona out of it?idk
# instead of having "interviewer" ? 

def open_convo_session(persona, message): 

    interlocutor_desc = "Interviewer"

    curr_convo += [[interlocutor_desc, line]]

    retrieved = retrieve(persona, [line], 50)[line]
    summarized_idea = generate_summarize_ideas(persona, retrieved, line)

    next_line = generate_next_line(persona, interlocutor_desc, curr_convo, summarized_idea)
    curr_convo += [[persona.scratch.name, next_line]]


def generate_summarize_ideas(persona, nodes, question): 
  statements = ""
  for n in nodes:
    statements += f"{n.embedding_key}\n"
  summarized_idea = run_gpt_prompt_summarize_ideas(persona, statements, question)[0]
  return summarized_idea



def generate_next_line(persona, interlocutor_desc, curr_convo, summarized_idea):
  # Original chat -- line by line generation 
  prev_convo = ""
  for row in curr_convo: 
    prev_convo += f'{row[0]}: {row[1]}\n'

  next_line = run_gpt_prompt_generate_next_convo_line(persona, 
                                                      interlocutor_desc, 
                                                      prev_convo, 
                                                      summarized_idea)[0]  
  return next_line


def chat(maze, persona, focused_event, reaction_mode, personas):
  init_persona = persona

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

    act_pronunciatio = "💬" 
    act_obj_description = None
    act_obj_pronunciatio = None
    act_obj_event = (None, None, None)

    _create_react(p, inserted_act, inserted_act_dur,
      act_address, act_event, chatting_with, convo, chatting_with_buffer, chatting_end_time,
      act_pronunciatio, act_obj_description, act_obj_pronunciatio, 
      act_obj_event, act_start_time)



















