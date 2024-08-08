"""
Given the persona, returns an integer that indicates the hour when the 
persona wakes up.  
"""

import sys
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API  
from LLM_Character.persona.persona import Persona
from LLM_Character.persona.prompt_templates.prompt import generate_prompt 

COUNTER_LIMIT = 5

def _create_prompt_input(persona:Persona)-> list[str]:
    prompt_input = [persona.scratch.get_str_iss(),
                persona.scratch.get_str_lifestyle(),
                persona.scratch.get_str_firstname()]
    return prompt_input

def _clean_up_response(response:str) -> int:
    cr = int(response.strip().lower().split("am")[0])
    return cr
 
def _validate_response(response:str) -> bool:
    try: 
        _clean_up_response(response)
    except: 
        return False
    return True

def run_prompt_wake_up(persona:Persona, model:LLM_API, verbose=False):
    prompt_template = "LLM_Character/persona/prompt_template/wake_up_hour.txt"
    prompt_input = _create_prompt_input(persona)
    prompt = generate_prompt(prompt_input, prompt_template)
    output = model.query_text(prompt)

    # NOTE: REPEAT UNTIL IT SPITS OUT A RESPONSE WITH THE CORRECT FORMAT 
    counter = 0
    while not _validate_response(output) and counter < COUNTER_LIMIT: 
        output = model.query_text(prompt)
        counter += 1
    output = _clean_up_response(output)

    # if verbose: 
    # print_run_prompts(prompt_template, persona, gpt_param, 
    #                   prompt_input, prompt, output)
    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms

    person = Persona("BARA")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc) 
    run_prompt_wake_up(person, model)
