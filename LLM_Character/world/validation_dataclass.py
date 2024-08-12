from pydantic import BaseModel 
from pydantic import field_validator
from typing import Optional

class BaseMessage(BaseModel):
    type: str

# class data sent from unity to python endpoint for sending chat messages. 
class PromptData(BaseModel):
    persona_name:str
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

# TODO
# pass all kinds of arenas, sectors, gameobject in the entire world, to this endpoint.
# pass all kind of character paramters, etc...
# all the data that normally resides in a json, that is stored on this python endpoint
# can also be sent dynamically from unity in order to initialise 
# the reverieserver and the persoans and the environment. 
# class SystemMessage(BaseMessage):
#     type: str
#     spatial_information:LocationData