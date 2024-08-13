from pydantic import BaseModel 
from pydantic import field_validator
from typing import Tuple, Optional, Any

class BaseMessage(BaseModel):
    type: str
    data: Any

# ---------------------------------------------------------------------------
# class data sent from unity to python endpoint for sending chat messages. 
class PromptData(BaseModel):
    persona_name:str
    message: str
    value: int

class PromptMessage(BaseMessage):
    type: str
    data: PromptData

# ---------------------------------------------------------------------------
# class data sent from unity to python endpoint for sending update data.
class GameObject(BaseModel):
    gameobject: str

class Arena(BaseModel):
    arena: str
    gameobjects: Optional[list[GameObject]] = None 

class Sector(BaseModel):
    sector: str
    arenas: Optional[list[Arena]] = None

class LocationData(BaseModel):
    world: str 
    sectors: list[Sector] 

class OneLocationData(BaseModel):
    world: str 
    sectors: Sector 

    @field_validator('sectors')
    def check_current_location(cls, value):
        sector_arenas = value.arenas
        if sector_arenas is None or len(sector_arenas) != 1:
            raise ValueError('sector in current location must contain exactly one arena.')
        return value

class UpdateMessage(BaseMessage):
    type: str
    # dict of persona names and their location
    data:  dict[str, OneLocationData]


# ---------------------------------------------------------------------------
# class data sent from unity to python endpoint for sending intial setup data.
class ScratchData(BaseModel):
    curr_time: str
    daily_plan_req:str
    name:str
    first_name:str
    last_name:str
    age:int
    innate:str
    learned:str
    currently:str
    lifestyle:str
    living_area: OneLocationData
    # there may be some parameters that could be added. 
    # ... see json file in generative agent repo
    recency_w:int
    relevance_w:int
    importance_w:int
    recency_decay:int
    importance_trigger_max:int
    importance_trigger_curr:int
    importance_ele_n:int
    # there may be some parameters that could be added. 
    # ... see json file in generative agent repo
    daily_req:list[str]
    f_daily_schedule:list[str]
    f_daily_schedule_hourly_org:list[str]
    # there may be some parameters that could be added. 
    # ... see json file in generative agent repo

    act_address: OneLocationData 
    act_start_time: str 
    act_duration: str  
    act_description: str 
    act_event: Tuple[str, str, str] # not sure 
    chatting_with: str 
    chat: list[list[str]] # converted to AI_Messages, or in the same format as AI_messages, nonetheless, it will be converted to some kind of list for serialisabiility.  
    # maybe make a different class for thsi chat type altogether, based on AI_Messages? idk 
    chatting_with_buffer: dict
    chatting_end_time: str 

class KwStrengthData(BaseModel):
    kw_strength_event: dict[str, int]
    kw_strength_thought: dict[str, int]

class Node(BaseModel):
    node_id: int
    node_count: int
    type_count: int
    type: str
    depth: int
    created: str
    expiration: Optional[str]
    subject: str
    predicate: str
    object: str
    description: str
    embedding_key: str
    poignancy: int
    keywords: list[str]
    filling: list[str]

class AssociativeMemoryData(BaseModel):
    embeddings: dict[str, list[float]]
    kw_strenght: KwStrengthData
    nodes: dict[str, Node]

class PersonaData(BaseModel):
    scratch_data:ScratchData
    spatial_data:LocationData
    as_mem_data:AssociativeMemoryData

class MetaData(BaseModel):
    fork_sim_code:str
    sim_code:str
    curr_time:str
    sec_per_step:int
    persona_names:list[str]
    step:int

class SetupData(BaseModel):
    meta:MetaData
    personas: dict[str, PersonaData]
    # NOTE: this extra field represent the entire possible virtual world (which can be moddeled after real places), it represent
    # the maze class that is in the original generative agent paper.
    # is not needed now, untill we decide to include perceiving into the agent.  
    virtual_world: LocationData

class SetupMessage(BaseMessage):
    type:str
    data: SetupData








