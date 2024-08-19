import copy
import json
from typing import Union

from LLM_Character.util import BASE_DIR
from LLM_Character.llm_api import LLM_API 

from LLM_Character.messages_dataclass import AIMessage, AIMessages
from LLM_Character.persona.prompt_modules.prompt import generate_prompt 
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory  
from LLM_Character.persona.memory_structures.associative_memory.concept_node import ConceptNode  

COUNTER_LIMIT = 5

def _create_prompt_input_1(uscratch:UserScratch, 
                         cscratch:PersonaScratch, 
                         ca_mem:AssociativeMemory, 
                         retrieved:dict[str, list[ConceptNode]], 
                         curr_context:str, 
                         curr_chat:list[AIMessage]): 

    prev_convo_insert = "\n"
    if ca_mem.seq_chat:
        for i in ca_mem.seq_chat: 
            if i.object == uscratch.name: 
                v1 = int((cscratch.curr_time - i.created).total_seconds()/60)
                prev_convo_insert += f'{str(v1)} minutes ago, {cscratch.name} and {uscratch.name} were already {i.description} This context takes place after that conversation.'
                break
    if prev_convo_insert == "\n": 
        prev_convo_insert = ""
    if ca_mem.seq_chat: 
        if int((cscratch.curr_time - ca_mem.seq_chat[-1].created).total_seconds()/60) > 480: 
            prev_convo_insert = ""

    curr_sector = f"{cscratch.get_curr_location()['sector']}"
    curr_arena= f"{cscratch.get_curr_location()['arena']}"
    curr_location = f"{curr_arena} in {curr_sector}"

    retrieved_str = ""
    for _, vals in retrieved.items(): 
        for v in vals: 
            retrieved_str += f"- {v.description}\n"

    convo_str = ""
    for i in curr_chat:
        convo_str += i.print_message_sender() + "\n"
    
    if convo_str == "": 
        convo_str = "[The conversation has not started yet -- start it!]"

    init_iss = f"Here is Here is a brief description of {cscratch.name}.\n{cscratch.get_str_iss()}"
    # FIXME; fix this shit, use one placeholder for each value...
    prompt_input = [init_iss, 
                    cscratch.name, 
                    retrieved_str, 
                    prev_convo_insert,
                    curr_location, 
                    curr_context, 
                    cscratch.name, 
                    uscratch.name,
                    convo_str, 
                    cscratch.name, 
                    uscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name,
                    cscratch.name
                    ]
    return prompt_input
def _create_prompt_input_2(cscratch:PersonaScratch, 
                         curr_chat:list[AIMessage]): 
    convo_str = ""
    for i in curr_chat:
        convo_str += i.print_message_sender() + "\n"
    
    if convo_str == "": 
        convo_str = "[The conversation has not started yet -- start it!]"

    prompt_input = [convo_str, 
                    cscratch.name]
    return prompt_input

def _clean_up_response_1(response:str) -> Union[None, dict[str,str]]:
    obj = extract_first_json_dict(response)
    if not obj :
        return None
    cleaned_dict = dict()
    cleaned = []
    for _, val in obj.items(): 
      cleaned += [val]
    cleaned_dict["utterance"] = cleaned[0]
    cleaned_dict["trust"] = cleaned[1]
    cleaned_dict["emotion"] = cleaned[2]
    return cleaned_dict

def _clean_up_response_2(response:str) -> Union[None, dict[str,str]]:
    obj = extract_first_json_dict(response)
    if not obj :
        return None
    cleaned_dict = dict()
    cleaned = []
    for _, val in obj.items(): 
      cleaned += [val]
    cleaned_dict["end"] = True 
    if "f" in str(cleaned[0]) or "F" in str(cleaned[0]): 
      cleaned_dict["end"] = False
    return cleaned_dict

def extract_first_json_dict(data_str:str) -> Union[None, dict[str,str]]:
    start_idx = data_str.find('{')
    end_idx = data_str.find('}', start_idx) + 1

    if start_idx == -1 or end_idx == 0:
        return None

    json_str = data_str[start_idx:end_idx]
    try:
        json_dict = json.loads(json_str)
        return json_dict
    except json.JSONDecodeError:
        return None

def _validate_response(output:str, clean_up_response:callable): 
    try: 
        return clean_up_response(output)
    except:
      return None

def _get_fail_safe(): 
    return {"utterance": "...", "end": False}

def _get_valid_output(model, prompt, clean_up_response:callable, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt).strip()
        success = _validate_response(output, clean_up_response)
        if success:
          return success
    return _get_fail_safe()

def run_prompt_iterative_chat(uscratch:UserScratch, 
                              cscratch:PersonaScratch, 
                              camem:AssociativeMemory, 
                              model:LLM_API, 
                              retrieved:dict[str, list[ConceptNode]], 
                              curr_context:str, 
                              curr_chat:list[AIMessage], 
                              verbose=False) -> Union[str, dict[str, str]]:
    prompt_template = BASE_DIR + "/LLM_Character/persona/prompt_modules/templates/iterative_convo.txt" 
    prompt_input = _create_prompt_input_1(uscratch, cscratch, camem, retrieved, curr_context, curr_chat)
    prompt = generate_prompt(prompt_input, prompt_template)
    
    am = AIMessages()
    am.add_message(prompt, None, "user", "system")
   
    output1 = _get_valid_output(model, am, _clean_up_response_1, COUNTER_LIMIT)

    message = output1["utterance"]
    new_chat = curr_chat + [AIMessage(cscratch.name, message, "user", "MessageAI")] 
    
    prompt_template = BASE_DIR + "/LLM_Character/persona/prompt_modules/templates/is_convo_ending.txt" 
    prompt_input = _create_prompt_input_2(cscratch, new_chat)
    prompt = generate_prompt(prompt_input, prompt_template)
    
    am = AIMessages()
    am.add_message(prompt, None, "user", "system")
    
    output2 = _get_valid_output(model, am, _clean_up_response_2, COUNTER_LIMIT)
    return output1, output2 

if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.persona.persona import Persona

    person = Persona("FRERO", "nice")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    # run_prompt_iterative_chat(Null,Null, Null, Null, Null, "", "")
