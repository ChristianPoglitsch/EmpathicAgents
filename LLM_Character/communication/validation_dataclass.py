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
    user_name:str
    message: str

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

class MoveMessage(BaseMessage):
    type: str
    # dict of persona names and their location
    data:  dict[str, OneLocationData]


# ---------------------------------------------------------------------------
# class data sent from unity to python endpoint for sending intial setup data.
class PersonaScratchData(BaseModel):
    curr_time: Optional[str]
    name: Optional[str]
    first_name:str
    last_name:str
    age:int
    innate:str
    learned:str
    currently:str
    lifestyle:str
    living_area: OneLocationData
    
    recency_w:int
    relevance_w:int
    importance_w:int
    recency_decay:int
    importance_trigger_max:int
    importance_trigger_curr:int
    importance_ele_n:int
    
class UserScratchData(BaseModel):
    name:str

class PersonaData(BaseModel):
    scratch_data:PersonaScratchData
    spatial_data:LocationData

class UserData(BaseModel):
    scratch_data: UserScratchData

class MetaData(BaseModel):
    fork_sim_code: Optional[str]
    sim_code:str
    curr_time:str
    sec_per_step:int
    persona_names:list[str]
    step:int

class UpdateData(BaseModel):
    meta:MetaData
    personas: dict[str, PersonaData]
    users: dict[str, UserData] 

class SetupData(BaseModel):
    fork_sim_code: Optional[str]
    sim_code:str

class SetupMessage(BaseMessage):
    type:str
    data: SetupData








