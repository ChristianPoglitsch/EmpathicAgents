from LLM_Character.persona.memory_structures.scratch.user_scratch import UserScratch 
from LLM_Character.persona.cognitive_modules.converse import chatting 

# User represents the human who plays the game.
class User: 
  scratch:UserScratch
  def __init__(self, name:str):
    self.scratch = UserScratch(name)
 
  def move(self, personas, curr_location, curr_time):
    self.scratch.curr_location = curr_location
    self.scratch.curr_time = curr_time

  def open_convo_session(self, data, model) -> str: 
    return chatting(self.scratch, data, model)



