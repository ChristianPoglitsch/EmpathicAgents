from LLM_Character.communication.incoming_messages import MetaData, FullPersonaData
from pydantic import BaseModel 
from typing import Any, Dict

class BaseResponse(BaseModel):
    type: str
    status : str
    data: Any
# ---------------------------------------------------------------------------
class ErrorResponse(BaseResponse):
    type: str # type of error for example, PromptResponseError etc.
    status:str 
    data: str # description of the error. 

# ---------------------------------------------------------------------------
class PromptResponseData(BaseModel):
    utt: str
    emotion : str
    trust_level : int 
    end: bool

class PromptReponse(BaseResponse):
    type: str
    status: str
    data: PromptResponseData 

# ---------------------------------------------------------------------------
class StartResponse(BaseResponse):
    type:str
    status:str
    data:str

# ---------------------------------------------------------------------------
class MoveResponseData(BaseModel):
    persona: Dict[str, Dict[str, Any]]
    meta: Dict[str, Any]

class MoveResponse(BaseResponse):
    type: str
    data: MoveResponseData


# ---------------------------------------------------------------------------

class GetPersonasResponse(BaseResponse):
    type : str
    data : list[str] 

class GetUsersResponse(BaseResponse):
    type : str
    data : list[str]

class GetPersonaDetailsResponse(BaseResponse):
    type : str
    data : FullPersonaData

class GetSavedGamesResponse(BaseResponse):
    type : str
    data : list[str]

class GetMetaDataResponse(BaseResponse):
    type : str
    data : MetaData 







