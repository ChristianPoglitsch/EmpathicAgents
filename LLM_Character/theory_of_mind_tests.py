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

    query_introduction = "I am going to tell you a short story about some people. At the end of this story a person will say or do something. When I have finished telling it I will ask you some questions about what happened in the story. The story is: John and Mary were sitting in the newspaper office, reading through a huge pile of hate mail. 'Obviously our readers liked your story', said John. Did John think the readers liked the story?"
    
    
    message = AIMessage(message=query_introduction, role="user", class_type="MessageAI", sender="user")
    messages = AIMessages()
    messages.add_message(message)

    model = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    # model_id = "genericgod/GerMerge-em-leo-mistral-v0.2-SLERP"

    # model = OpenAIComms()
    # model_id = "gpt-4o"

    model.init(model_id)
    wrapped_model = LLM_API(model)
    model.max_tokens = 100
    
    model2 = OpenAIComms()
    model_id2 = "gpt-4o"
    model2.init(model_id2)
    wrapped_model2 = LLM_API(model2)
    model2.max_tokens = 100
    
    query_result = wrapped_model2.query_text(messages)
    print("Answer")
    print(query_result)    

    query_instruction_analye = "Is the answer for this question correct. Question:'" + query_introduction + "' Answer:'" + query_result + "'"
    message = AIMessage(message=query_instruction_analye, role="user", class_type="MessageAI", sender="user")
    messages = AIMessages()
    messages.add_message(message)    
    query_result_analyse = wrapped_model.query_text(messages)

    print("Analysed answer")
    print(query_result_analyse)
