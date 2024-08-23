from dataclasses import dataclass
import random
from typing import Dict
from LLM_Character.communication.incoming_messages import EventData
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory, ConceptNode
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.cognitive_modules.retrieving.util import *

@dataclass
class EventContext :
  curr_event : ConceptNode
  events : list[ConceptNode] 
  thoughts : list[ConceptNode]

def retrieve_contextual_events(a_mem:AssociativeMemory, perceived:list[ConceptNode]) ->  Dict[str, EventContext]:
  retrieved = dict()
  for event in perceived: 
    relevant_events = a_mem.retrieve_relevant_events(event.subject, event.predicate, event.object) # return set of ConceptNode
    relevant_thoughts = a_mem.retrieve_relevant_thoughts(event.subject, event.predicate, event.object) # return set of ConceptNode

    context = EventContext(
        curr_event=event,
        events=list(relevant_events),
        thoughts=list(relevant_thoughts)
    )        
    retrieved[event.description] = context

  return retrieved

def retrieve_focal_points(scratch: PersonaScratch,
             a_mem: AssociativeMemory, 
             focal_points: list[str], 
             model:LLM_API, 
             n_count=30) -> dict[str, list[ConceptNode]]:
    retrieved = dict()
    for focal_pt in focal_points:
        nodes = retrieve_recent_sorted_nodes(a_mem)
        
        recency_out = extract_recency(scratch, nodes)
        recency_out = normalize_dict_floats(recency_out, 0, 1)

        importance_out = extract_importance(nodes)
        importance_out = normalize_dict_floats(importance_out, 0, 1)

        relevance_out = extract_relevance(a_mem, nodes, focal_pt, model)
        relevance_out = normalize_dict_floats(relevance_out, 0, 1)

        gw = [0.5, 3, 2]
        master_out = dict()
        for key in recency_out.keys():
            master_out[key] = (scratch.recency_w*recency_out[key]*gw[0]
                               + scratch.relevance_w *
                               relevance_out[key]*gw[1]
                               + scratch.importance_w*importance_out[key]*gw[2])

        master_out = top_highest_x_values(master_out, n_count)
        master_nodes = [a_mem.id_to_node[key]
                        for key in list(master_out.keys())]

        for n in master_nodes:
            n.last_accessed = scratch.curr_time
        retrieved[focal_pt] = master_nodes
    return retrieved
   


if __name__ == "__main__":
    from LLM_Character.persona.persona import Persona
    from LLM_Character.llm_comms.llm_openai import OpenAIComms
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.util import BASE_DIR
    
    import datetime

    # modelc = LocalComms()
    # model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    # modelc.init(model_id)
    
    modelc = OpenAIComms()
    model_id = "gpt-4"
    modelc.init(model_id)
    
    model = LLM_API(modelc)

    person = Persona("Camila")
    person.load_from_file(BASE_DIR + "/LLM_Character/storage/localhost/default/personas/Camila")
    text = "Frederiek went to the shop"  
    created = datetime.datetime(21,3,4)
    expiration= None
    s = "Lorem"
    p = "went" 
    o = "shop"
    description = "frederiek went to the shop" 
    keywords = "shop" 
    poignancy = 3
    embedding_pair = [description, model.get_embedding(description)]
    filling = None 

    # person.a_mem.add_chat(created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)
    node1 = person.a_mem.add_thought(created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)
    node2 = person.a_mem.add_event(created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)
    
    retrieved1 = retrieve_focal_points(person.scratch, person.a_mem, ["who is me?"], model)
    print(len(retrieved1["who is me?"]))
    print(retrieved1["who is me?"][0].description)
    print(retrieved1["who is me?"][1].description)
    
    
    retrieved2 = retrieve_contextual_events(person.a_mem, [node1, node2])
    print(retrieved2)



    