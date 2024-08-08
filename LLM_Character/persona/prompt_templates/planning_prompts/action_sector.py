import sys
sys.path.append('../../../')

from abc import ABC, abstractmethod

from LLM_Character.llm_api import LLM_API 
from persona.persona import Persona
from persona.prompt_templates.prompt import RunPrompt


class ActionSector(RunPrompt):
    """
    Given the action description, persona, 
    return the suitable sector where this action can take place.   
    """
    def _create_prompt_input(self, action_description:str, persona:Persona): 
       
        # GATHER ALL THE NECASSARY INFORMATION. 
        act_world = persona.scratch.get_curr_location()['world']
        act_sector = persona.scratch.get_curr_location()['sector']
        domicile = persona.scratch.get_living_area()['sector']
        name = persona.scratch.get_str_name()
       
        possible_sectors = persona.s_mem.get_str_accessible_sectors(act_world)
        possible_arenas = persona.s_mem.get_str_accessible_sector_arenas(act_world, domicile)
       
        daily_plan = persona.scratch.get_str_daily_plan_req() 
        action_description_1, action_description_2 = self._decomp_action_desc(action_description)
        
        # PUT ALL THE NECESSARY INFORMATION INTO A LIST, IN THE RIGHT ORDER ACCORDING TO THE PROMPT TEMPLATE. 
        prompt_input = []
        prompt_input += [name]
        prompt_input += [domicile]
        prompt_input += [possible_arenas]
        prompt_input += [name]
        prompt_input += [act_sector]
        prompt_input += [possible_arenas]
        #TODO: check if this is correct, normaliter, zou er geen \n als dailyplan "" leeg is, ma kdenk kan geen kwaad. 
        prompt_input += [f"\n{daily_plan}"]
        #TODO: we moeten ons geen zorgen maken of de available sector in iemand anders zijn huis is, want we werken maar in 1 scene.
        # geen zorgen hierover, in ons geval.  
        prompt_input += [possible_sectors]

        prompt_input += [name]
        prompt_input += [action_description_1]

        prompt_input += [action_description_2]
        prompt_input += [name]

        return prompt_input

    def _decomp_action_desc(self, action_description:str):
        if "(" in action_description: 
            action_description_1 = action_description.split("(")[0].strip()
            action_description_2 = action_description.split("(")[-1][:-1]
            return action_description_1, action_description_2
        else : 
            return action_description, action_description

    def _clean_up_response(self, response:str):
        pass
     
    def _validate_response(self, response:str):
        pass
 
    def run_prompt(self, persona:Persona, model:LLM_API, verbose=False):
        # model.safe_generate_response
        pass




if __name__ == "__main__":
    x = ActionSector()
    pass













def run_gpt_prompt_action_sector(action_description, 
                                persona, 
                                maze, 
                                test_input=None, 
                                verbose=False):
  def create_prompt_input(action_description, persona, maze, test_input=None): 
    act_world = f"{maze.access_tile(persona.scratch.curr_tile)['world']}"
    
    prompt_input = []
    
    prompt_input += [persona.scratch.get_str_name()]
    prompt_input += [persona.scratch.living_area.split(":")[1]]
    x = f"{act_world}:{persona.scratch.living_area.split(':')[1]}"
    prompt_input += [persona.s_mem.get_str_accessible_sector_arenas(x)]


    prompt_input += [persona.scratch.get_str_name()]
    prompt_input += [f"{maze.access_tile(persona.scratch.curr_tile)['sector']}"]
    x = f"{act_world}:{maze.access_tile(persona.scratch.curr_tile)['sector']}"
    prompt_input += [persona.s_mem.get_str_accessible_sector_arenas(x)]

    if persona.scratch.get_str_daily_plan_req() != "": 
      prompt_input += [f"\n{persona.scratch.get_str_daily_plan_req()}"]
    else: 
      prompt_input += [""]


    # MAR 11 TEMP
    accessible_sector_str = persona.s_mem.get_str_accessible_sectors(act_world)
    curr = accessible_sector_str.split(", ")
    fin_accessible_sectors = []
    for i in curr: 
      if "'s house" in i: 
        if persona.scratch.last_name in i: 
          fin_accessible_sectors += [i]
      else: 
        fin_accessible_sectors += [i]
    accessible_sector_str = ", ".join(fin_accessible_sectors)
    # END MAR 11 TEMP

    prompt_input += [accessible_sector_str]



    action_description_1 = action_description
    action_description_2 = action_description
    if "(" in action_description: 
      action_description_1 = action_description.split("(")[0].strip()
      action_description_2 = action_description.split("(")[-1][:-1]
    prompt_input += [persona.scratch.get_str_name()]
    prompt_input += [action_description_1]

    prompt_input += [action_description_2]
    prompt_input += [persona.scratch.get_str_name()]
    return prompt_input

