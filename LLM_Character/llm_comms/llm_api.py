from LLM_Character.llm_comms.llm_abstract import LLMComms
from LLM_Character.messages_dataclass import AIMessages


class LLM_API:
    """
    A class to handle operations related to LLM models,
    including loading models, querying models
    """

    def __init__(self, LLMComms: LLMComms):
        self._model = LLMComms

    def query_text(self, message: AIMessages) -> str:
        return self._model.send_text(message)

    def get_embedding(self, text: str) -> list[float]:
        """
        retrieves the text embedding.
        """
        return self._model.send_embedding(text)
