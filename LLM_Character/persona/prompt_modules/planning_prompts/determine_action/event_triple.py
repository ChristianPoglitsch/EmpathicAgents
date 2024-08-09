"""
Given the action description, persona, 
return the suitable tuple (subject, predicate, object) of the action description. 
"""
import sys
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API 
from LLM_Character.persona.persona import Persona
import LLM_Character.persona.prompt_templates.prompt as p 

COUNTER_LIMIT = 5

def _create_prompt_input(action_description:str, 
                         persona:Persona): 
    p_name = persona.scratch.get_str_name()

    if "(" in action_description: 
      action_description = action_description.split("(")[-1].split(")")[0]

    prompt_input = [p_name, 
                    action_description,
                    p_name]
    return prompt_input

def _clean_up_response(response:str):
    cr = response.strip()
    cr = [i.strip() for i in cr.split(")")[0].split(",")]
    return cr

def _validate_response(response:str): 
    try: 
      gpt_response = _clean_up_response(response)
      if len(gpt_response) != 2: 
        return False
    except: return False
    return True 

def _get_fail_safe(persona:Persona): 
    p_name = persona.scratch.get_str_name()
    fs = (p_name, "is", "idle")
    return fs

def _get_valid_output(persona, model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt)
        if _validate_response(output):
            return _clean_up_response(output)
    return _get_fail_safe(persona)

def run_prompt_action_sector(persona:Persona, 
                             model:LLM_API, 
                             action_description:str,
                             verbose=False):
    prompt_template = "LLM_Character/persona/prompt_template/generate_event_triple.txt"
    prompt_input = _create_prompt_input(action_description, persona)
    prompt = p.generate_prompt(prompt_input, prompt_template)
    output = _get_valid_output(persona, model, prompt, COUNTER_LIMIT)

    p_name = persona.scratch.get_str_name()
    output = (p_name, output[0], output[1])

    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    person = Persona("FRERO")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    run_prompt_action_sector(person, 
                             model, 
                             "i will drive to the broeltorens.")

