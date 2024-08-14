# run_prompt_summarize_conversation
import json
import sys


sys.path.append('../../../')

from LLM_Character.llm_api import LLM_API 
import LLM_Character.persona.prompt_modules.prompt as p 
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch

COUNTER_LIMIT = 5

def _create_prompt_input(conversation): 
    convo_str = ""
    for row in conversation: 
      convo_str += f'{row[0]}: "{row[1]}"\n'

    prompt_input = [convo_str]
    return prompt_input

def _clean_up_response(response:str):
     return "conversing about " + response.strip()

def _validate_response(output:str): 
    try: 
        return _clean_up_response(output)
    except:
      return None

# FIXME: not a good default i thik 
def _get_fail_safe(): 
    return "conversing with a housemate about morning greetings"

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt).strip()
        success = _validate_response(output)
        if success:
          return success
    return _get_fail_safe()

def run_prompt_summarize_conversation(model:LLM_API, 
                                      conversation, 
                                      verbose=False):
    prompt_template = "persona/prompt_template/summarize_conversation.txt" 
    prompt_input = _create_prompt_input(conversation)
    prompt = p.generate_prompt(prompt_input, prompt_template)
    
    # FIXME: 
    # example_output = "conversing about what to eat for lunch" ########
    # special_instruction = "The output must continue the sentence above by filling in the <fill in> tag. Don't start with 'this is a conversation about...' Just finish the sentence but do not miss any important details (including who are chatting)." ########


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
    run_prompt_summarize_conversation(model, "i will drive to the broeltorens.")

