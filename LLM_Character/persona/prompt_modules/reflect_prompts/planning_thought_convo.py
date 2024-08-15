import sys
sys.path.append('../../../../')

from LLM_Character.llm_api import LLM_API 
import LLM_Character.persona.prompt_modules.prompt as p 
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch

COUNTER_LIMIT = 5

def _create_prompt_input(scratch:PersonaScratch, all_utt:str): 
    prompt_input = [all_utt, scratch.name, scratch.name, scratch.name]
    return prompt_input

def _clean_up_response(response:str):
    return response.split('"')[0].strip()

def _validate_response(response:str): 
    try: 
      return _clean_up_response(response)
    except:
      return None

def _get_fail_safe(): 
    return "..."

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt)
        if _validate_response(output):
            return _clean_up_response(output)
    return _get_fail_safe()

def run_prompt_planning_thought_convo(
        scratch:PersonaScratch, 
        model:LLM_API, 
        all_utt:str , 
        verbose=False):
    prompt_template = "persona/prompt_template/planning_thought_convo.txt"
    prompt_input = _create_prompt_input(scratch, all_utt)
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
    run_prompt_planning_thought_convo(person.scratch, model, "i will drive to the broeltorens.")



