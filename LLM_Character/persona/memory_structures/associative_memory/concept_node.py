import sys
sys.path.append('../../')

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