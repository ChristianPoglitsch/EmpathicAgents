import json


class ConceptNode: 
  def __init__(self,
               node_id, node_count, type_count, node_type, depth,
               created, expiration, 
               s, p, o, 
               description, embedding_key, poignancy, keywords, filling): 
    self.node_id = node_id
    self.node_count = node_count
    self.type_count = type_count
    self.type = node_type # thought / chat
    self.depth = depth

    self.created = created
    self.expiration = expiration
    self.last_accessed = self.created

    self.subject = s
    self.predicate = p
    self.object = o

    self.description = description
    self.embedding_key = embedding_key
    self.poignancy = poignancy
    self.keywords = keywords
    self.filling = filling


def spo_summary(self): 
  return (self.subject, self.predicate, self.object)


class AssociativeMemory: 
  def __init__(self, f_saved:str): 
    self.id_to_node:dict[str, ConceptNode]= dict()

    self.seq_thought:list[ConceptNode] = []
    self.seq_chat:list[ConceptNode] = []

    self.kw_to_thought:dict[str, list[ConceptNode]] = dict()
    self.kw_to_chat:dict[str, list[ConceptNode]] = dict()

    self.kw_strength_thought:dict[str, int] = dict()

    self.embeddings:dict[str, list[float]] = json.load(open(f_saved + "/embeddings.json"))


  def add_thought(self, created, expiration, s, p, o, 
                        description, keywords, poignancy, 
                        embedding_pair, filling):
    # Setting up the node ID and counts.
    node_count = len(self.id_to_node.keys()) + 1
    type_count = len(self.seq_thought) + 1
    node_type = "thought"
    node_id = f"node_{str(node_count)}"
    depth = 1 
    try: 
      if filling: 
        depth += max([self.id_to_node[i].depth for i in filling])
    except: 
      pass

    # Creating the <ConceptNode> object.
    node = ConceptNode(node_id, node_count, type_count, node_type, depth,
                       created, expiration, 
                       s, p, o, 
                       description, embedding_pair[0], poignancy, keywords, filling)

    # Creating various dictionary cache for fast access. 
    self.seq_thought[0:0] = [node]
    keywords = [i.lower() for i in keywords]
    for kw in keywords: 
      if kw in self.kw_to_thought: 
        self.kw_to_thought[kw][0:0] = [node]
      else: 
        self.kw_to_thought[kw] = [node]
    self.id_to_node[node_id] = node 

    # Adding in the kw_strength
    if f"{p} {o}" != "is idle":  
      for kw in keywords: 
        if kw in self.kw_strength_thought: 
          self.kw_strength_thought[kw] += 1
        else: 
          self.kw_strength_thought[kw] = 1

    self.embeddings[embedding_pair[0]] = embedding_pair[1]

    return node


  def add_chat(self, created, expiration, s, p, o, 
                     description, keywords, poignancy, 
                     embedding_pair, filling): 
    # Setting up the node ID and counts.
    node_count = len(self.id_to_node.keys()) + 1
    type_count = len(self.seq_chat) + 1
    node_type = "chat"
    node_id = f"node_{str(node_count)}"
    depth = 0

    # Creating the <ConceptNode> object.
    node = ConceptNode(node_id, node_count, type_count, node_type, depth,
                       created, expiration, 
                       s, p, o, 
                       description, embedding_pair[0], poignancy, keywords, filling)

    # Creating various dictionary cache for fast access. 
    self.seq_chat[0:0] = [node]
    keywords = [i.lower() for i in keywords]
    for kw in keywords: 
      if kw in self.kw_to_chat: 
        self.kw_to_chat[kw][0:0] = [node]
      else: 
        self.kw_to_chat[kw] = [node]
    self.id_to_node[node_id] = node 

    self.embeddings[embedding_pair[0]] = embedding_pair[1]
        
    return node

