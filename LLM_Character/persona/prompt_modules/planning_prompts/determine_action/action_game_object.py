"""
Given the action description, persona, 
return the suitable gameobject where this action can take place.   
"""
import sys
import random
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API 
import LLM_Character.persona.prompt_modules.prompt as p 
from LLM_Character.persona.memory_structures.scratch.scratch import Scratch
from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
COUNTER_LIMIT = 5

def _create_prompt_input(scratch:Scratch, 
                         s_mem:MemoryTree,
                         action_description:str, 
                         act_sector:str, 
                         act_arena:str): 
    # NOTE world < sectors < arenas < gameobjects
    act_world = scratch.get_curr_location()['world']
    possible_go = s_mem.get_str_accessible_arena_game_objects(act_world,
                                                                      act_sector, 
                                                                      act_arena)

    if "(" in action_description: 
      action_description = action_description.split("(")[-1][:-1]

    prompt_input = []
    prompt_input += [action_description]
    prompt_input += [possible_go]

    return prompt_input

def _validate_response(response:str): 
    if len(response.strip()) < 1: 
        return False
    return True

def _clean_up_response(response:str):
    cleaned_response = response.strip()
    return cleaned_response

def _get_fail_safe(): 
    fs = ("bed")
    return fs

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt)
        if _validate_response(output):
            return _clean_up_response(output)
    return _get_fail_safe()

def run_prompt_action_game_object(scratch:Scratch,
                                  s_mem: MemoryTree, 
                                  model:LLM_API, 
                                  action_description:str,
                                  action_sector:str,
                                  action_arena:str, 
                                  verbose=False):
    prompt_template = "LLM_Charact/persona/prompt_template/action_game_object.txt"
    prompt_input = _create_prompt_input(scratch, s_mem, action_description, action_sector, action_arena)
    prompt = p.generate_prompt(prompt_input, prompt_template)
    output = _get_valid_output(model, prompt, COUNTER_LIMIT)

    act_world = scratch.get_curr_location()['world']
    possible_go = s_mem.get_str_accessible_arena_game_objects(act_world,
                                                                      action_sector, 
                                                                      action_arena)
    x = [i.strip() for i in possible_go.split(",")]
    if output not in x: 
        output = random.choice(x)

    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.persona.persona import Persona

    person = Persona("FRERO")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    run_prompt_action_game_object(person, 
                             model, 
                             "i will drive to the broeltorens.", 
                             "kortrijk",
                             "kortrijk centrum")



