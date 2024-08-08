"""
The long term planning that spans a day. 
"""

import sys
import datetime
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API  
from LLM_Character.persona.persona import Persona
import LLM_Character.persona.prompt_templates.prompt as p 

COUNTER_LIMIT = 5

def _component_statements(retrieved):
    statements = ""
    for _, val in retrieved.items():
        for i in val: 
          statements += f"{i.created.strftime('%A %B %d -- %H:%M %p')}: {i.embedding_key}\n"
    return statements

def _create_prompt_input(persona:Persona, retrieved:int)-> tuple[list[str], list[str]]:
    stmts = _component_statements(retrieved)
    p_name = persona.scratch.name 
    time = persona.scratch.curr_time.strftime('%A %B %d') 

    plan_input = []
    plan_input += [stmts]
    plan_input+= [p_name]
    plan_input+= [time]

    thought_prompt = []
    thought_prompt += [stmts] 
    thought_prompt += [p_name] 
    return plan_input, thought_prompt

def _create_prompt_input_2(persona:Persona, plan_note:str, thought_note:str) -> list[str]:

    stmts   = _component_statements(retrieved)
    p_name  = persona.scratch.name 
    time    = persona.scratch.curr_time.strftime('%A %B %d') 
    time_diff = (persona.scratch.curr_time - datetime.timedelta(days=1)).strftime('%A %B %d')
    currently = persona.scratch.currently
    notes = (plan_note + thought_note).replace('\n', '')

    currently_prompt = []
    currently_prompt += [stmts] 
    currently_prompt += [p_name]
    currently_prompt += [time_diff]
    currently_prompt += [currently]
    currently_prompt += [notes]
    currently_prompt += [time] 

    return currently_prompt  
def _create_prompt_input_3(persona:Persona) -> list[str]:
    commonset = persona.scratch.get_str_iss()
    curr_time = persona.scratch.curr_time.strftime('%A %B %d')
    p_name  = persona.scratch.name 

    daily_req_prompt  = []
    daily_req_prompt += [commonset]
    daily_req_prompt += [curr_time]
    daily_req_prompt += [p_name]
    
    return daily_req_prompt

def _get_valid_output(model, prompt, counter_limit):
    return model.query_text(prompt)

def run_prompt_revise_identity(persona:Persona, model:LLM_API, retrieved,verbose=False):
    prompt_template_1 = "LLM_Character/persona/prompt_template/revise_identity_1.txt"
    prompt_template_2 = "LLM_Character/persona/prompt_template/revise_identity_2.txt"
    prompt_input1, prompt_input2 = _create_prompt_input(persona, retrieved)
    prompt1 = p.generate_prompt(prompt_input1, prompt_template_1)
    prompt2 = p.generate_prompt(prompt_input2, prompt_template_2)
    plan_note = _get_valid_output(model, prompt1, COUNTER_LIMIT)
    thought_note = _get_valid_output(model, prompt2, COUNTER_LIMIT)
    
    prompt_template_3 = "LLM_Character/persona/prompt_template/revise_identity_3.txt"
    prompt_input3 = _create_prompt_input_2(persona, plan_note, thought_note)
    prompt = p.generate_prompt(prompt_input3, prompt_template_3 )
    currently_note = _get_valid_output(model, prompt, COUNTER_LIMIT)
    
    prompt_template_4 = "LLM_Character/persona/prompt_template/revise_identity_4.txt"
    prompt_input4 = _create_prompt_input_3(persona)
    prompt = p.generate_prompt(prompt_input4, prompt_template_4 )
    daily_req_note = _get_valid_output(model, prompt, COUNTER_LIMIT)
    new_daily_req = daily_req_note.replace('\n', ' ')
    
    return plan_note, thought_note, currently_note, new_daily_req


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms

    person = Persona("BARA")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    
    # TODO replace retrived with actual dictionary with some list of conceptNodes as values  
    retrieved = None
    run_prompt_revise_identity(person, model, retrieved)





  persona.scratch.currently = new_currently

  daily_req_prompt = persona.scratch.get_str_iss() + "\n"
  daily_req_prompt += f"Today is {persona.scratch.curr_time.strftime('%A %B %d')}. Here is {persona.scratch.name}'s plan today in broad-strokes (with the time of the day. e.g., have a lunch at 12:00 pm, watch TV from 7 to 8 pm).\n\n"
  daily_req_prompt += f"Follow this format (the list should have 4~6 items but no more):\n"
  daily_req_prompt += f"1. wake up and complete the morning routine at <time>, 2. ..."

  new_daily_req = ChatGPT_single_request(daily_req_prompt)
  new_daily_req = new_daily_req.replace('\n', ' ')
  print ("WE ARE HERE!!!", new_daily_req)
  persona.scratch.daily_plan_req = new_daily_req
