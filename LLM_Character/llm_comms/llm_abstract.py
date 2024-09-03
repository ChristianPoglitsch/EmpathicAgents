from abc import ABC, abstractmethod

from LLM_Character.messages_dataclass import AIMessages


class LLMComms(ABC):
    @abstractmethod
    def init():
        pass

    @abstractmethod
    def send_text(self, prompt: AIMessages, max_length=100):
        pass

    @abstractmethod
    def send_embedding(text: str):
        pass

    @abstractmethod
    def set_params():
        pass
