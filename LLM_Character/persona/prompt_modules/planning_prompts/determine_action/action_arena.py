"""
Given the action description, persona, 
return the suitable arenas where this action can take place.   
"""
import sys
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API 
import LLM_Character.persona.prompt_modules.prompt as p 
from LLM_Character.persona.memory_structures.scratch import Scratch
from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
COUNTER_LIMIT = 5

def _create_prompt_input(scratch:Scratch, s_mem:MemoryTree, action_description:str, act_sector:str): 
    name = scratch.get_str_name()

    # NOTE world < sectors < arenas < gameobjects
    act_world = scratch.get_curr_location()['world']
    possible_arenas = s_mem.get_str_accessible_sector_arenas(act_world, act_sector)
    action_description_1, action_description_2 = _decomp_action_desc(action_description)

    prompt_input = []
    prompt_input += [name]
    prompt_input += [act_sector]
    prompt_input += [possible_arenas]
    prompt_input += [name]
    prompt_input += [action_description_1]
    prompt_input += [action_description_2]
    prompt_input += [act_sector]
    prompt_input += [possible_arenas]

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

def run_prompt_action_arena(scratch:Scratch, s_mem:MemoryTree, model:LLM_API, action_description:str,action_sector:str, verbose=False):
    prompt_template = "LLM_Character/persona/prompt_template/action_sector.txt"
    prompt_input = _create_prompt_input(scratch, s_mem,  action_description, action_sector)
    prompt = p.generate_prompt(prompt_input, prompt_template)
    output = _get_valid_output(model, prompt, COUNTER_LIMIT)

    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.persona.persona import Persona

    person = Persona("FRERO")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    run_prompt_action_arena(person, model, "i will drive to the broeltorens.", "kortrijk" )




