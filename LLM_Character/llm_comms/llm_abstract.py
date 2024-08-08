from abc import ABC, abstractmethod

class LLMComms(ABC):
    @abstractmethod
    def init():
        pass
    
    @abstractmethod
    def send_text(self, message:str):
        pass

    @abstractmethod
    def send_embedding():
        pass

    @abstractmethod
    def set_params():
        pass
