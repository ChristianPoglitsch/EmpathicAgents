import logging

from LLM_Character.communication.comm_medium import CommMedium
from LLM_Character.communication.message_processor import MessageProcessor
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.messages_dataclass import AIMessage, AIMessages
from LLM_Character.util import LOGGER_NAME, setup_logging

logger = logging.getLogger(LOGGER_NAME)


if __name__ == "__main__":
    setup_logging("python_server_endpoint")
    import torch

    from LLM_Character.llm_comms.llm_openai import OpenAIComms
    from LLM_Character.llm_comms.llm_local import LocalComms

    logger.info("CUDA found " + str(torch.cuda.is_available()))

    #message = AIMessage(message="Who are you?", role="user", class_type="MessageAI", sender="user")
    message = AIMessage(message="Hallo, wer bist du?", role="user", class_type="MessageAI", sender="user")
    messages = AIMessages()
    messages.add_message(message)
    

    model = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    model_id = "genericgod/GerMerge-em-leo-mistral-v0.2-SLERP"

    #model = OpenAIComms()
    #model_id = "gpt-4"

    model.init(model_id)
    wrapped_model = LLM_API(model)
    
    result = wrapped_model.query_text(messages)

    print(result)
    
