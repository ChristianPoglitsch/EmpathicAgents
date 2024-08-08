"""
Given the action description, persona, 
return the suitable arenas where this action can take place.   
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
    domicile = persona.scratch.get_living_area()['sector']
    name = persona.scratch.get_str_name()
   
    possible_sectors = persona.s_mem.get_str_accessible_sectors(act_world)
    possible_arenas = persona.s_mem.get_str_accessible_sector_arenas(act_world, domicile)
   
    daily_plan = persona.scratch.get_str_daily_plan_req() 
    action_description_1, action_description_2 = _decomp_action_desc(action_description)

    action_description_1 = action_description
    action_description_2 = action_description
    if "(" in action_description: 
      action_description_1 = action_description.split("(")[0].strip()
      action_description_2 = action_description.split("(")[-1][:-1]
    
  #FIXME: HIER ZAK IK, TE CHECKEN MET DE ECHTE VERSIE OF DA ALLES HIER STAAT. 

    prompt_input = []
    prompt_input += [name]
    prompt_input += [domicile]
    prompt_input += [possible_arenas]
    prompt_input += [name]

    prompt_input += [action_description_1]
    prompt_input += [action_description_2]
    prompt_input += [name]
    prompt_input += [act_sector]

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
        # output = random.choice(x)
        output = persona.scratch.get_living_area()['sector']

    # if debug or verbose: 
    # print_run_prompts(prompt_template, persona, gpt_param, 
    #                   prompt_input, prompt, output)
    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    person = Persona("FRERO")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc) 
    run_prompt_action_sector(person, model, "i will drive to the broeltorens.")









def run_gpt_prompt_action_arena(action_description, 
                                persona, 
                                maze, act_world, act_sector,
                                test_input=None, 
                                verbose=False):
  def create_prompt_input(action_description, persona, maze, act_world, act_sector, test_input=None): 
    prompt_input = []
    # prompt_input += [persona.scratch.get_str_name()]
    # prompt_input += [maze.access_tile(persona.scratch.curr_tile)["arena"]]
    # prompt_input += [maze.access_tile(persona.scratch.curr_tile)["sector"]]
    prompt_input += [persona.scratch.get_str_name()]
    x = f"{act_world}:{act_sector}"
    prompt_input += [act_sector]

    # MAR 11 TEMP
    accessible_arena_str = persona.s_mem.get_str_accessible_sector_arenas(x)
    curr = accessible_arena_str.split(", ")
    fin_accessible_arenas = []
    for i in curr: 
      if "'s room" in i: 
        if persona.scratch.last_name in i: 
          fin_accessible_arenas += [i]
      else: 
        fin_accessible_arenas += [i]
    accessible_arena_str = ", ".join(fin_accessible_arenas)
    # END MAR 11 TEMP


    prompt_input += [accessible_arena_str]


    action_description_1 = action_description
    action_description_2 = action_description
    if "(" in action_description: 
      action_description_1 = action_description.split("(")[0].strip()
      action_description_2 = action_description.split("(")[-1][:-1]
    prompt_input += [persona.scratch.get_str_name()]
    prompt_input += [action_description_1]

    prompt_input += [action_description_2]
    prompt_input += [persona.scratch.get_str_name()]

    

    prompt_input += [act_sector]

    prompt_input += [accessible_arena_str]
    # prompt_input += [maze.access_tile(persona.scratch.curr_tile)["arena"]]
    # x = f"{maze.access_tile(persona.scratch.curr_tile)['world']}:{maze.access_tile(persona.scratch.curr_tile)['sector']}:{maze.access_tile(persona.scratch.curr_tile)['arena']}"
    # prompt_input += [persona.s_mem.get_str_accessible_arena_game_objects(x)]

    
    return prompt_input

  def __func_clean_up(gpt_response, prompt=""):
    cleaned_response = gpt_response.split("}")[0]
    return cleaned_response

  def __func_validate(gpt_response, prompt=""): 
    if len(gpt_response.strip()) < 1: 
      return False
    if "}" not in gpt_response:
      return False
    if "," in gpt_response: 
      return False
    return True
  
  def get_fail_safe(): 
    fs = ("kitchen")
    return fs

  gpt_param = {"engine": "text-davinci-003", "max_tokens": 15, 
               "temperature": 0, "top_p": 1, "stream": False,
               "frequency_penalty": 0, "presence_penalty": 0, "stop": None}
  prompt_template = "persona/prompt_template/v1/action_location_object_vMar11.txt"
  prompt_input = create_prompt_input(action_description, persona, maze, act_world, act_sector)
  prompt = generate_prompt(prompt_input, prompt_template)

  fail_safe = get_fail_safe()
  output = safe_generate_response(prompt, gpt_param, 5, fail_safe,
                                   __func_validate, __func_clean_up)
  print (output)
  # y = f"{act_world}:{act_sector}"
  # x = [i.strip() for i in persona.s_mem.get_str_accessible_sector_arenas(y).split(",")]
  # if output not in x: 
  #   output = random.choice(x)

  if debug or verbose: 
    print_run_prompts(prompt_template, persona, gpt_param, 
                      prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]




















