import sys
sys.path.append('../../')

from abc import ABC, abstractmethod

from LLM_Character.llm_api import HuggingFace 
from persona.persona import Persona

class RunPrompt(ABC) :
  
    @abstractmethod 
    def create_prompt_input(self, persona:Persona):
        pass

    @abstractmethod 
    def clean_up_response(self, response:str):
        pass
    
    @abstractmethod 
    def validate_response(self, response:str):
        pass

    @abstractmethod 
    def run_prompt(self, persona:Persona, model:HuggingFace, verbose=False):
        # model.safe_generate_response
        pass


if __name__ == "__main__":
    # Can't instantiate abstract class 
    # x = RunPrompt()
    pass