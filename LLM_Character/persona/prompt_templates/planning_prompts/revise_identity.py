"""
The long term planning that spans a day. 
"""

import sys
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

def _clean_up_response(response, prompt=""):
    return response 
def _validate_response(response:str) -> bool:
    try: 
        _clean_up_response(response)
    except: 
        return False
    return True

def _get_fail_safe(): 
    return None

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt)
        if _validate_response(output):
            return _clean_up_response(output)
    return _get_fail_safe()

def run_prompt_revise_identity(persona:Persona, model:LLM_API, retrieved,verbose=False):
    prompt_template = "LLM_Character/persona/prompt_template/revise_identity.txt"
    prompt_input1, prompt_input2 = _create_prompt_input(persona, retrieved)
    prompt1 = p.generate_prompt(prompt_input1, prompt_template)
    prompt2 = p.generate_prompt(prompt_input2, prompt_template)
    plan_note = _get_valid_output(model, prompt1, COUNTER_LIMIT)
    thought_note = _get_valid_output(model, prompt2, COUNTER_LIMIT)
    
    return plan_note, thought_note
    # return output, [output, prompt, prompt_input]


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





# def run_prompt_revise_identity(persona, model:LLM_API): 
#
#     currently_prompt = f"{p_name}'s status from {(persona.scratch.curr_time - datetime.timedelta(days=1)).strftime('%A %B %d')}:\n"
#     currently_prompt += f"{persona.scratch.currently}\n\n"
#     currently_prompt += f"{p_name}'s thoughts at the end of {(persona.scratch.curr_time - datetime.timedelta(days=1)).strftime('%A %B %d')}:\n" 
#     currently_prompt += (plan_note + thought_note).replace('\n', '') + "\n\n"
#     currently_prompt += f"It is now {persona.scratch.curr_time.strftime('%A %B %d')}. Given the above, write {p_name}'s status for {persona.scratch.curr_time.strftime('%A %B %d')} that reflects {p_name}'s thoughts at the end of {(persona.scratch.curr_time - datetime.timedelta(days=1)).strftime('%A %B %d')}. Write this in third-person talking about {p_name}."
#     currently_prompt += f"If there is any scheduling information, be as specific as possible (include date, time, and location if stated in the statement).\n\n"
#     currently_prompt += "Follow this format below:\nStatus: <new status>"
#     # print ("DEBUG ;adjhfno;asdjao;asdfsidfjo;af", p_name)
#     # print (currently_prompt)
#     new_currently = ChatGPT_single_request(currently_prompt)
#     # print (new_currently)
#     # print (new_currently[10:])
#
#
#
#     return new_currently  
