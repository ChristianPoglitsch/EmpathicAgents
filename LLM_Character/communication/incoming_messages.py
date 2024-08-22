from pydantic import BaseModel, field_validator 
from typing import Any, Dict, List, Optional

class BaseMessage(BaseModel):
    type: str
    data: Any



# ---------------------------------------------------------------------------
# PUTTERS/ POSTERS 
# ---------------------------------------------------------------------------


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
class LocationDetails(BaseModel):
    details: List[str]

class Location(BaseModel):
    location: Dict[str, LocationDetails]

class City(BaseModel):
    city: Dict[str, Location]

class LocationData(BaseModel):
    cities: Dict[str, City]

class OneLocationData(BaseModel):
    world: str 
    sector: str
    arena : Optional[str] = None
    obj : Optional[str] = None

class EventData(BaseModel):
    action_event_subject : Optional[str]= None
    action_event_predicate : Optional[str]= None
    action_event_object : Optional[str]= None
    action_event_description : Optional[str]= None

class PerceivingData(BaseModel):
    name : str
    curr_loc : OneLocationData
    events: list[EventData]
    
class MoveMessage(BaseMessage):
    type: str
    data:  list[PerceivingData]

# ---------------------------------------------------------------------------
# class data sent from unity to python endpoint for sending updated data.
class PersonaScratchData(BaseModel):
    curr_location: Optional[OneLocationData] = None
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

class PersonaData(BaseModel):
    name: str
    scratch_data: Optional[PersonaScratchData] = None
    spatial_data: Optional[LocationData] = None

class UserData(BaseModel):
    old_name : str
    name: str

class MetaData(BaseModel):
    curr_time: Optional[str] = None
    sec_per_step: Optional[int] = None

class UpdateMetaMessage(BaseMessage):
    type:str
    data: MetaData 

class UpdatePersonaMessage(BaseMessage):
    type:str
    data: PersonaData 

class UpdateUserMessage(BaseMessage):
    type:str
    data: UserData 

# ---------------------------------------------------------------------------
# class data sent from unity to python endpoint for sending intial setup data.
class StartData(BaseModel):
    fork_sim_code: Optional[str]
    sim_code:str

class StartMessage(BaseMessage):
    type:str
    data: StartData

# ---------------------------------------------------------------------------
# https://stackoverflow.com/questions/67699451/make-every-field-as-optional-with-pydantic
class FullPersonaScratchData(BaseModel):
    curr_location: OneLocationData 
    first_name: str 
    last_name: str 
    age: int
    innate: str 
    learned: str 
    currently: str 
    lifestyle: str 
    living_area: OneLocationData
    
    recency_w: int 
    relevance_w: int 
    importance_w: int 
    recency_decay: int 
    importance_trigger_max: int 
    importance_trigger_curr: int 
    importance_ele_n: int 

class FullPersonaData(BaseModel):
    name:str
    scratch_data : FullPersonaScratchData
    spatial_data: LocationData

class AddPersonaMessage(BaseMessage):
    type: str
    data: FullPersonaData


# ---------------------------------------------------------------------------
# GETTERS
# ---------------------------------------------------------------------------


class GetPersonasMessage(BaseMessage):
    type : str
    data : None

class GetUsersMessage(BaseMessage):
    type : str
    data : None

class PersonID(BaseModel):
    name : str

class GetPersonaDetailsMessage(BaseMessage):
    type : str
    data : PersonID 

class GetSavedGamesMessage(BaseMessage):
    type : str
    data : None

class GetMetaDataMessage(BaseMessage):
    type : str
    data : None
                    