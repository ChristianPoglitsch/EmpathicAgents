from pydantic import BaseModel 
from typing import Any

class BaseMessage(BaseModel):
    type: str
    data: Any

# ---------------------------------------------------------------------------
class StartSavedGamesData(BaseModel):
    saved_games: list[str] # list of fork sim codes that can be forked from.

class StartSavedGamesMessage(BaseMessage):
    type:str
    data: StartSavedGamesData 


# ---------------------------------------------------------------------------
class PromptResponseData(BaseModel):
    utt: str
    emotion : str
    trust_level : str 

class PromptReponseMessage(BaseMessage):
    type: str
    data: PromptResponseData 

