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

def _create_prompt_input(uscratch:UserScratch, 
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
                    uscratch.name
                    ]
    return prompt_input

def _clean_up_response(response:str) -> Union[None, dict[str,str]]:
    obj = extract_first_json_dict(response)
    if not obj :
        return None
    cleaned_dict = dict()
    cleaned = []
    for _, val in obj.items(): 
      cleaned += [val]
    cleaned_dict["utterance"] = cleaned[0]
    cleaned_dict["end"] = True
    if "f" in str(cleaned[1]) or "F" in str(cleaned[1]): 
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

def _validate_response(output:str): 
    try: 
        return _clean_up_response(output)
    except:
      return None

def _get_fail_safe(): 
    return {"utterance": "...", "end": False}

def _get_valid_output(model, prompt, counter_limit):
    for _ in range(counter_limit):
        output = model.query_text(prompt).strip()
        success = _validate_response(output)
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
    prompt_input = _create_prompt_input(uscratch, cscratch, camem, retrieved, curr_context, curr_chat)
    prompt = generate_prompt(prompt_input, prompt_template)
    print("prompt")
    print(prompt)
    am = AIMessages()
    am.add_message(prompt, None, "user", "system")
    output = _get_valid_output(model, am, COUNTER_LIMIT)
    print("output")
    print(output)
    return output 

if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.persona.persona import Persona

    person = Persona("FRERO", "nice")

    modelc = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    # run_prompt_iterative_chat(Null,Null, Null, Null, Null, "", "")
