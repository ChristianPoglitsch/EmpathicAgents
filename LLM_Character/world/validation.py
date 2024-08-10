from pydantic import BaseModel 
from pydantic import field_validator

from typing import Optional

class BaseMessage(BaseModel):
    type: str

# class data sent from unity to python endpoint for sending chat messages. 
class PromptData(BaseModel):
    message: str
    value: int

class PromptMessage(BaseMessage):
    type: str
    data: PromptData

# class data sent from unity to python endpoint for sending intial setup data.
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

class SystemMessage(BaseMessage):
    type: str
    character_name:str
    current_location:LocationData
    spatial_information:LocationData

    @field_validator('current_location')
    def check_current_location(cls, value):
        sectors = value.sectors
        if len(sectors) != 1:
            raise ValueError('current location must contain exactly one sector.')
        sector = next(iter(sectors.values()))
        sector_arenas = sector.arenas
        if sector_arenas is None or len(sector_arenas) != 1:
            raise ValueError('sector in current location must contain exactly one arena.')
        return value


