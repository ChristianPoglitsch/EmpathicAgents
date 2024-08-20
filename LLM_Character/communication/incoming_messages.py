from pydantic import BaseModel, field_validator 
from typing import Any, Dict, List, Optional

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
# class data sent from unity to python endpoint for sending updated data.
class PersonaScratchData(BaseModel):
    curr_time: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    innate: Optional[str] = None
    learned: Optional[str] = None
    currently: Optional[str] = None
    lifestyle: Optional[str] = None
    living_area: Optional[OneLocationData] = None
    
    recency_w: Optional[int] = None
    relevance_w: Optional[int] = None
    importance_w: Optional[int] = None
    recency_decay: Optional[int] = None
    importance_trigger_max: Optional[int] = None
    importance_trigger_curr: Optional[int] = None
    importance_ele_n: Optional[int] = None

class UserScratchData(BaseModel):
    name: Optional[str] = None

class PersonaData(BaseModel):
    scratch_data: Optional[PersonaScratchData] = None
    spatial_data: Optional[LocationData] = None

class UserData(BaseModel):
    scratch_data: Optional[UserScratchData] = None

class MetaData(BaseModel):
    curr_time: Optional[str] = None
    sec_per_step: Optional[int] = None
    persona_names: Optional[List[str]] = None
    step: Optional[int] = None

class UpdateData(BaseModel):
    meta: Optional[MetaData] = None
    personas: Optional[Dict[str, PersonaData]] = None
    users: Optional[Dict[str, UserData]] = None

class UpdateMessage(BaseMessage):
    type:str
    data: UpdateData 

# ---------------------------------------------------------------------------
# class data sent from unity to python endpoint for sending intial setup data.
class StartData(BaseModel):
    fork_sim_code: Optional[str]
    sim_code:str

class StartMessage(BaseMessage):
    type:str
    data: StartData

