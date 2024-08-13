import sys
sys.path.append('../../')

from numpy.linalg import norm
from numpy import dot

from LLM_Character.llm_api import LLM_API
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory, ConceptNode
from LLM_Character.persona.memory_structures.scratch.scratch import Scratch

def retrieve(scratch:Scratch, a_mem: AssociativeMemory, focal_points: list[str], model:LLM_API, n_count=30):
    retrieved = dict()
    for focal_pt in focal_points:
        nodes = _retrieve_recent_sorted_nodes(a_mem)

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

        # FIXME: why is the following line needed??
        # master_out = top_highest_x_values(master_out, len(master_out.keys()))
        master_out = top_highest_x_values(master_out, n_count)
        master_nodes = [a_mem.id_to_node[key]
                        for key in list(master_out.keys())]

        for n in master_nodes:
            n.last_accessed = scratch.curr_time
        retrieved[focal_pt] = master_nodes
    return retrieved


def _retrieve_recent_sorted_nodes(a_mem: AssociativeMemory):
    # FIXME: WHY NOT RETRIEVE FROM SEQ_CHAT ?
    nodes = []
    for i in a_mem.seq_thought:
        if "idle" not in i.embedding_key:
            nodes += [[i.last_accessed, i]]

    nodes = sorted(nodes, key=lambda x: x[0])
    nodes = [i for _, i in nodes]
    return nodes


def extract_recency(scratch:Scratch, nodes:list[ConceptNode]):
    recency_vals = [scratch.recency_decay ** i
                    for i in range(1, len(nodes) + 1)]

    recency_out = dict()
    for count, node in enumerate(nodes):
        recency_out[node.node_id] = recency_vals[count]
    return recency_out


def extract_importance(nodes:list[ConceptNode]):
    importance_out = dict()
    for _ , node in enumerate(nodes):
        importance_out[node.node_id] = node.poignancy
    return importance_out


def extract_relevance(a_mem:AssociativeMemory, nodes:list[ConceptNode], focal_pt:str, model: LLM_API):
    focal_embedding = model.semantic_meaning(focal_pt)
    relevance_out = dict()
    for _, node in enumerate(nodes):
        node_embedding = a_mem.embeddings[node.embedding_key]
        relevance_out[node.node_id] = cos_sim(node_embedding, focal_embedding)
    return relevance_out


def cos_sim(a:list[float], b:list[float]):
    return dot(a, b)/(norm(a)*norm(b))


def normalize_dict_floats(d: dict, target_min: float, target_max: float):
    min_val = min(val for val in d.values())
    max_val = max(val for val in d.values())
    range_val = max_val - min_val

    if range_val == 0:
        for key, val in d.items():
            d[key] = (target_max - target_min)/2
    else:
        for key, val in d.items():
            d[key] = ((val - min_val) * (target_max - target_min)
                      / range_val + target_min)
    return d


def top_highest_x_values(d:dict, x:int):
    top_v = dict(sorted(d.items(),
                        key=lambda item: item[1],
                        reverse=True)[:x])
    return top_v


if __name__ == "__main__":
    import datetime
    from llm_comms.llm_local import LocalComms
    from persona import Persona

    person:Persona = Persona("FREDERIEK", "nice")
    text = "Frederiek went to the shop"  
    created = datetime.datetime(21,3,4)
    expiration= None
    s = "Lorem"
    p = "went" 
    o = "shop"
    description = "frederiek went to the shop" 
    keywords = "shop" 
    poignancy = 3 
    embedding_pair = [description, [1,2,3]]
    filling = None 

    person.a_mem.add_chat(created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)
    person.a_mem.add_thought(created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)
	
    modelc = LocalComms()

    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelc.init(model_id)

    model = LLM_API(modelc)
    retrieved = retrieve(person, ["who is me?"], model)

