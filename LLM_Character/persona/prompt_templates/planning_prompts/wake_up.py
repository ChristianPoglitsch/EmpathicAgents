
import sys
sys.path.append('../../../')

from abc import ABC, abstractmethod

from huggingface import HuggingFace 
from persona.persona import Persona
from persona.prompt_templates.prompt import RunPrompt


class WakeUp(RunPrompt):
    def create_prompt_input(self, persona:Persona):
        pass
 
    def clean_up_response(self, response:str):
        pass
     
    def validate_response(self, response:str):
        pass
 
    def run_prompt(self, persona:Persona, model:HuggingFace, verbose=False):
        # model.safe_generate_response
        pass


if __name__ == "__main__":
    x = WakeUp()
    pass


# def run_gpt_prompt_wake_up_hour(persona, test_input=None, verbose=False): 
#   """
#   Given the persona, returns an integer that indicates the hour when the 
#   persona wakes up.  

#   INPUT: 
#     persona: The Persona class instance 
#   OUTPUT: 
#     integer for the wake up hour.
#   """
#   def create_prompt_input(persona:Persona, test_input=None): 
#     if test_input: return test_input
#     prompt_input = [persona.scratch.get_str_iss(),
#                     persona.scratch.get_str_lifestyle(),
#                     persona.scratch.get_str_firstname()]
#     return prompt_input

#   def __func_clean_up(gpt_response, prompt=""):
#     cr = int(gpt_response.strip().lower().split("am")[0])
#     return cr
  
#   def __func_validate(gpt_response, prompt=""): 
#     try: __func_clean_up(gpt_response, prompt="")
#     except: return False
#     return True

#   def get_fail_safe(): 
#     fs = 8
#     return fs

#   gpt_param = {"engine": "text-davinci-002", "max_tokens": 5, 
#              "temperature": 0.8, "top_p": 1, "stream": False,
#              "frequency_penalty": 0, "presence_penalty": 0, "stop": ["\n"]}
#   prompt_template = "persona/prompt_template/v2/wake_up_hour_v1.txt"
#   prompt_input = create_prompt_input(persona, test_input)
#   prompt = generate_prompt(prompt_input, prompt_template)
#   fail_safe = get_fail_safe()

#   output = safe_generate_response(prompt, gpt_param, 5, fail_safe,
#                                    __func_validate, __func_clean_up)
  
#   if debug or verbose: 
#     print_run_prompts(prompt_template, persona, gpt_param, 
#                       prompt_input, prompt, output)
    
#   return output, [output, prompt, gpt_param, prompt_input, fail_safe]
