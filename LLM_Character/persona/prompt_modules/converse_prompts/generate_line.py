import json
import sys
sys.path.append('../../../')

from LLM_Character.llm_api import LLM_API 
from LLM_Character.persona.persona import Persona
import LLM_Character.persona.prompt_modules.prompt as p 

COUNTER_LIMIT = 5

def _create_prompt_input(persona, 
                         interlocutor_desc, 
                         prev_convo, 
                         retrieved_summary): 
 
    name = persona.scratch.get_str_name()
    commonset = persona.scratch.get_str_iss()
    prompt_input = [name, 
                    commonset, 
                    name, 
                    interlocutor_desc, 
                    prev_convo, 
                    retrieved_summary, 
                    name]
    return prompt_input

def _clean_up_response(response:str):
    return response.split('"')[0].strip()

def _validate_response(output:str): 
    try: 
        end_index = output.rfind('}') + 1
        curr_response = output[:end_index]
        output = json.loads(curr_response)["output"]
        return _clean_up_response(output)
    except:
      return None

def _get_fail_safe(): 
    return "..."

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt).strip()
        success = _validate_response(output)
        if success:
          return success
    return _get_fail_safe()

# FIXME: interlocutor_desc should be 'unkown' first. 
# then querry LLM and see if they know who 
# they are by qeurying their previous conversation
# and extracting the necessary information. 
def run_prompt_generate_next_conv_line(persona:Persona, 
                                       model:LLM_API, 
                                       prev_convo, 
                                       retrieved_summary, 
                                       verbose=False):

    prompt_template = "persona/prompt_template/generate_next_convo_line.txt"
    prompt_input = _create_prompt_input(persona, interlocutor_desc, prev_convo, retrieved_summary)
    prompt = p.generate_prompt(prompt_input, prompt_template)
    output = _get_valid_output(model, prompt, COUNTER_LIMIT)

    return output, [output, prompt, prompt_input]


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    person = Persona("FRERO", "nice")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    run_prompt_generate_next_conv_line(person, model, "i will drive to the broeltorens.", "kortrijk" )

