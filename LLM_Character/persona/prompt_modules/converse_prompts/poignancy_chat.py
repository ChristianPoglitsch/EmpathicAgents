import json
import sys
import datetime

sys.path.append('../../../')

from LLM_Character.llm_api import LLM_API 
import LLM_Character.persona.prompt_modules.prompt as p 
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch

COUNTER_LIMIT = 5


def _create_prompt_input(scratch:PersonaScratch): 
    prompt_input = [scratch.name,
                    scratch.get_str_iss(),
                    scratch.name,
                    scratch.act_description]
    return prompt_input

def _clean_up_response(response:str):
    return int(response.strip()) 

def _validate_response(output:str): 
    try: 
       return _clean_up_response(output)  
    except: 
      return None 

def  _get_fail_safe(): 
    return 4 

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt).strip()
        success = _validate_response(output)
        if success:
          return success
    return _get_fail_safe()

def run_prompt_poignancy_chat(cscratch:PersonaScratch, 
                                model:LLM_API, 
                                verbose=False):
    prompt_template = "persona/prompt_template/poignancy_chat.txt"
    prompt_input = _create_prompt_input(cscratch) 
#   example_output = "5" ########
#   special_instruction = "The output should ONLY contain ONE integer value on the scale of 1 to 10." ########
    prompt = p.generate_prompt(prompt_input, prompt_template)
    output = _get_valid_output(model, prompt, COUNTER_LIMIT)

    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.persona.persona import Persona

    person = Persona("FRERO", "nice")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    run_prompt_poignancy_chat(person.scratch, model)





