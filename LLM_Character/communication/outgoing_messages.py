from enum import Enum
from LLM_Character.communication.incoming_messages import MetaData, FullPersonaData
from pydantic import BaseModel
from typing import Any, Dict


class ResponseType(Enum):
    STARTRESPONSE = "StartResponse"
    PROMPTRESPONSE = "PromptResponse"
    MOVERESPONSE = "MoveResponse"


class StatusType(Enum):
    SUCCESS = "Success"
    FAIL = "Failed"


class BaseResponse(BaseModel):
    type: ResponseType
    status: StatusType
    data: Any
# ---------------------------------------------------------------------------


class ErrorResponse(BaseResponse):
    data: str  # description of the error.

# ---------------------------------------------------------------------------


class PromptResponseData(BaseModel):
    utt: str
    emotion: str
    trust_level: int
    end: bool


class PromptReponse(BaseResponse):
    data: PromptResponseData

# ---------------------------------------------------------------------------


class StartResponse(BaseResponse):
    data: str

# ---------------------------------------------------------------------------


class MoveResponseData(BaseModel):
    persona: Dict[str, Dict[str, Any]]
    meta: Dict[str, Any]


class MoveResponse(BaseResponse):
    data: MoveResponseData


# ---------------------------------------------------------------------------

class GetPersonasResponse(BaseResponse):
    data: list[str]


class GetUsersResponse(BaseResponse):
    data: list[str]


class GetPersonaDetailsResponse(BaseResponse):
    data: FullPersonaData


class GetSavedGamesResponse(BaseResponse):
    data: list[str]


class GetMetaDataResponse(BaseResponse):
    data: MetaData
