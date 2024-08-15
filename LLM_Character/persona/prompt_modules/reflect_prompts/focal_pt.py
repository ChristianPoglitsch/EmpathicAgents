import sys
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API 
import LLM_Character.persona.prompt_modules.prompt as p 
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch

COUNTER_LIMIT = 5

def _create_prompt_input(n:int, statements:str): 
    prompt_input = [statements, str(n)]
    return prompt_input

def _clean_up_response(response:str):
    response = "1) " + response.strip()
    ret = []
    for i in response.split("\n"): 
      ret += [i.split(") ")[-1]]
    return ret

def _validate_response(response:str): 
    try: 
      return _clean_up_response(response)
    except:
      return None

def _get_fail_safe(n): 
    return ["Who am I"] * n

# FIXME change in each for loop the paramters of the model for example, like in the other repo.
# if needed
def _get_valid_output(model, prompt, n, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt)
        if _validate_response(output):
            return _clean_up_response(output)
    return _get_fail_safe(n)

def run_prompt_generate_focal_pt(
        model:LLM_API,
        n:int,
        all_utt:str , 
        verbose=False):

    prompt_template = "persona/prompt_template/generate_focal_pt.txt"
    prompt_input = _create_prompt_input(n, all_utt)
    prompt = p.generate_prompt(prompt_input, prompt_template)
  # example_output = '["What should Jane do for lunch", "Does Jane like strawberry", "Who is Jane"]' ########
  # special_instruction = "Output must be a list of str." ########
    output = _get_valid_output(model, prompt, n, COUNTER_LIMIT)

    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.persona.persona import Persona

    person = Persona("FRERO", "nice")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc) 
    run_prompt_memo_convo(person.scratch, model, "i will drive to the broeltorens.")



