import sys
sys.path.append('../../')

from persona import Persona
from LLM_Character.llm_api import LLM_API 

def _retrieve_recent_sorted_nodes(persona:Persona):
  # FIXME: WHY NOT RETRIEVE FROM SEQ_CHAT ?
  nodes = [] 
  for i in persona.a_mem.seq_thought :
    if "idle" not in i.embedding_key :
      nodes += [[i.last_accessed, i]]

  nodes = sorted(nodes, key=lambda x: x[0])
  nodes = [i for _ , i in nodes]
  return nodes 

def retrieve(persona:Persona, focal_points:list[str], n_count=30): 
  retrieved = dict() 
  for focal_pt in focal_points: 
    nodes = _retrieve_recent_sorted_nodes(persona)

    recency_out = extract_recency(persona, nodes)
    recency_out = normalize_dict_floats(recency_out, 0, 1)

    importance_out = extract_importance(persona, nodes)
    importance_out = normalize_dict_floats(importance_out, 0, 1)  

    relevance_out = extract_relevance(persona, nodes, focal_pt)
    relevance_out = normalize_dict_floats(relevance_out, 0, 1)

    gw = [0.5, 3, 2]
    master_out = dict()
    for key in recency_out.keys(): 
      master_out[key] = (persona.scratch.recency_w*recency_out[key]*gw[0] 
                     + persona.scratch.relevance_w*relevance_out[key]*gw[1] 
                     + persona.scratch.importance_w*importance_out[key]*gw[2])

    # FIXME: why is the following line needed??
    # master_out = top_highest_x_values(master_out, len(master_out.keys()))
    master_out = top_highest_x_values(master_out, n_count)
    master_nodes = [persona.a_mem.id_to_node[key] 
                    for key in list(master_out.keys())]

    for n in master_nodes: 
      n.last_accessed = persona.scratch.curr_time
    retrieved[focal_pt] = master_nodes
  return retrieved

def extract_recency(persona, nodes):
  recency_vals = [persona.scratch.recency_decay ** i 
                  for i in range(1, len(nodes) + 1)]
  
  recency_out = dict()
  for count, node in enumerate(nodes): 
    recency_out[node.node_id] = recency_vals[count]

  return recency_out

def extract_importance(persona, nodes):
  importance_out = dict()
  for count, node in enumerate(nodes): 
    importance_out[node.node_id] = node.poignancy

  return importance_out

def extract_relevance(persona, nodes, focal_pt): 
  focal_embedding = get_embedding(focal_pt)

  relevance_out = dict()
  for count, node in enumerate(nodes): 
    node_embedding = persona.a_mem.embeddings[node.embedding_key]
    relevance_out[node.node_id] = cos_sim(node_embedding, focal_embedding)

  return relevance_out

def normalize_dict_floats(d, target_min, target_max):
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

def top_highest_x_values(d, x):
  top_v = dict(sorted(d.items(), 
                      key=lambda item: item[1], 
                      reverse=True)[:x])
  return top_v
