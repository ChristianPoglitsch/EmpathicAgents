from LLM_Character.communication.incoming_messages import MetaData, PersonaData
from pydantic import BaseModel 
from typing import Any

class BaseMessage(BaseModel):
    type: str
    data: Any

# ---------------------------------------------------------------------------
class PromptResponseData(BaseModel):
    utt: str
    emotion : str
    trust_level : str 

class PromptReponse(BaseMessage):
    type: str
    data: PromptResponseData 

# ---------------------------------------------------------------------------

class GetPersonasResponse(BaseMessage):
    type : str
    data : list[str] 

class GetUsersResponse(BaseMessage):
    type : str
    data : list[str]

class GetPersonaDetailsResponse(BaseMessage):
    type : str
    data : PersonaData

class GetSavedGamesResponse(BaseMessage):
    type : str
    data : list[str]

class GetMetaDataResponse(BaseMessage):
    type : str
    data : MetaData 







