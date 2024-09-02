from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel

from LLM_Character.communication.incoming_messages import FullPersonaData, MetaData


class ResponseType(Enum):
    START_RESPONSE = "StartResponse"
    PROMPT_RESPONSE = "PromptResponse"
    MOVE_RESPONSE = "MoveResponse"
    ERROR_RESPONSE = "ErrorResponse"

    GET_PERSONAS_RESPONSE = "GetPersonasRespons"
    GET_USERS_RESPONSE = "GetUsersResponse"
    GET_PERSONA_RESPONSE = "GetPersonaResponse"
    GET_SAVED_GAMES_RESPONSE = "GetSavedGamesResponse"
    GET_META_RESPONSE = "GetMetaResponse"


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
