from LLM_Character.llm_comms.llm_api import LLM_API 

from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
from LLM_Character.communication.incoming_messages import OneLocationData

def perceive(character_scratch:PersonaScratch,
             character_amem:AssociativeMemory, 
             character_smem: MemoryTree,
             locationData:OneLocationData,
             model:LLM_API):
    
     
    character_smem.update_oloc(locationData)
    
    
    return None