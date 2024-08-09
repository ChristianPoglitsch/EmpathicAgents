"""
Given the action description, persona, 
return the suitable sector where this action can take place.   
"""
import sys
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API 
from LLM_Character.persona.persona import Persona
import LLM_Character.persona.prompt_templates.prompt as p 

COUNTER_LIMIT = 5

def _create_prompt_input(action_description:str, persona:Persona): 
   
    act_world = persona.scratch.get_curr_location()['world']
    act_sector = persona.scratch.get_curr_location()['sector']
    liv_sector = persona.scratch.get_living_area()['sector']
    name = persona.scratch.get_str_name()
   
    # NOTE world < sectors < arenas < gameobjects
    possible_arenas1 = persona.s_mem.get_str_accessible_sector_arenas(act_world, liv_sector)
    possible_arenas2 = persona.s_mem.get_str_accessible_sector_arenas(act_world, act_sector)
    possible_sectors = persona.s_mem.get_str_accessible_sectors(act_world)
    
    daily_plan = persona.scratch.get_str_daily_plan_req() 
    action_description_1, action_description_2 = _decomp_action_desc(action_description)
    
    prompt_input = []
    prompt_input += [name]
    prompt_input += [liv_sector]
    prompt_input += [possible_arenas1]
    prompt_input += [name]
    prompt_input += [act_sector]
    prompt_input += [possible_arenas2]
    prompt_input += [f"\n{daily_plan}"]
    prompt_input += [possible_sectors]

    prompt_input += [name]
    prompt_input += [action_description_1]

    prompt_input += [action_description_2]
    prompt_input += [name]

    return prompt_input

def _decomp_action_desc(action_description:str):
    if "(" in action_description: 
        action_description_1 = action_description.split("(")[0].strip()
        action_description_2 = action_description.split("(")[-1][:-1]
        return action_description_1, action_description_2
    else : 
        return action_description, action_description

def _clean_up_response(response:str):
    cleaned_response = response.split("}")[0]
    return cleaned_response

def _validate_response(response:str): 
    if len(response.strip()) < 1: 
      return False
    if "}" not in response:
      return False
    if "," in response: 
      return False
    return True

def _get_fail_safe(): 
    fs = ("kitchen")
    return fs

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt)
        if _validate_response(output):
            return _clean_up_response(output)
    return _get_fail_safe()

def run_prompt_action_sector(persona:Persona, model:LLM_API, action_description:str, verbose=False):
    prompt_template = "LLM_Character/persona/prompt_template/action_sector.txt"
    prompt_input = _create_prompt_input(action_description, persona)
    prompt = p.generate_prompt(prompt_input, prompt_template)
    output = _get_valid_output(model, prompt, COUNTER_LIMIT)

    y = persona.scratch.curr_location['world']
    x = [i.strip() for i in persona.s_mem.get_str_accessible_sectors(y).split(",")]
    if output not in x: 
        output = persona.scratch.get_living_area()['sector']

    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    person = Persona("FRERO")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc) 
    run_prompt_action_sector(person, model, "i will drive to the broeltorens.")


