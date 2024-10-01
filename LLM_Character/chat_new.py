import logging

from LLM_Character.communication.comm_medium import CommMedium
from LLM_Character.communication.message_processor import MessageProcessor
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.messages_dataclass import AIMessage, AIMessages
from LLM_Character.util import LOGGER_NAME, setup_logging

logger = logging.getLogger(LOGGER_NAME)

# ---

from abc import ABC, abstractmethod
from copy import deepcopy
import re

class MessageStruct():

    def __init__(self, instruction : AIMessage):
        self._instruction = instruction
        self._chat_history = AIMessages()
        
    def add_message(self, message : AIMessage):
        self._chat_history.add_message(message)
        
    def get_instruction(self) -> AIMessage:
        return self._instruction
    
    def set_instruction(self, instruction : AIMessage):
        self._instruction = instruction
        
    def get_history(self) -> AIMessages:
        return self._chat_history
        
    def get_instruction_and_history(self) -> AIMessages:
        if len(self._chat_history.get_messages()) > 5:
            self._chat_history.remove_item(0)
            self._chat_history.remove_item(0)

        inctruction_with_history = AIMessages()
        inctruction_with_history.add_message(self._instruction)
        for item in self._chat_history.get_messages():
            inctruction_with_history.add_message(item)
        return inctruction_with_history
        
class MessageProcessing(ABC):
    
    def __init__(self, decorator):
        self._decorator = decorator

    @abstractmethod
    def get_messages(self) -> MessageStruct:
        pass

class BaseDecorator(MessageProcessing):
    def __init__(self, messageStruct : MessageStruct):
        self._message_struct = messageStruct
    
    def get_messages(self) -> MessageStruct:
        return deepcopy(self._message_struct)

class ImportanceDecorator(MessageProcessing):
    
    def __init__(self, decorator : MessageProcessing, llm_api : LLM_API):
        super(ImportanceDecorator, self).__init__(decorator)      
        self._llm_api = llm_api
        self._important_message = AIMessages()

    def get_messages(self) -> MessageStruct:
        message_processing = self._decorator.get_messages()
        messages = message_processing.get_history().get_messages()
        
        if len(messages) < 3:
            return message_processing
        
        message = 'Your role is an AI bot. Based on the Instruction meassure the importance of the Message. Score the importance in range of [0, 10]. Only reply with the score. For example reply with Score: 5.\n'
        message = message + 'Instruction:\n' + message_processing.get_instruction().get_message() + '\n'    
        message = message + 'Message:\n' + messages[-3].message + '\n' 
        
        ai_message = AIMessage(message=message, role="user", class_type="MessageAI", sender="user")
        ai_messages = AIMessages()
        ai_messages.add_message(ai_message)        
        self._llm_api.set_max_tokens(3)
        reply = self._llm_api.query_text(ai_messages)
        
        importance = re.findall(r'\d+', reply)
        importance = int(importance[-1])        
        if importance > 3:
            self._important_message.add_message(messages[-3])
            self._important_message.add_message(messages[-2])            

        print('--- ---')
        print('Importance: ' + reply)
        print('--- ---')
        
        m = message_processing.get_instruction()
        for item in self._important_message.get_messages():
            m.message = m.message + '\nImportant message of the past:' + item.message + ' from ' + item.sender
        message_processing.set_instruction(m)
        
        return message_processing

class EmotionDecorator(MessageProcessing):
    
    def __init__(self, decorator : MessageProcessing, llm_api : LLM_API):
        super(EmotionDecorator, self).__init__(decorator)      
        self._llm_api = llm_api

    def get_messages(self) -> MessageStruct:
        message_processing = self._decorator.get_messages()        
        messages = message_processing.get_history().get_messages()
        
        message = 'Your role is an AI bot. Based on the Instruction meassure the emotional state regarding the Message. Estimate the emotional state with one of the emotions: happy, angry, disgust, fear, surprise, sad or neutral. Only reply the emotion. \n'
        message = message + 'Instruction:\n' + message_processing.get_instruction().get_message() + '\n'    
        message = message + 'Message:\n' + messages[-1].message + '\n' 
        
        ai_message = AIMessage(message=message, role="user", class_type="MessageAI", sender="user")
        ai_messages = AIMessages()
        ai_messages.add_message(ai_message)
        
        self._llm_api.set_max_tokens(3)
        reply = self._llm_api.query_text(ai_messages)
        print('--- ---')
        print('Emotion: ' + reply)
        print('--- ---')
        m = message_processing.get_instruction()
        m.message = m.message + '\nHow you feel:' + reply
        message_processing.set_instruction(m)

        self._llm_api.set_max_tokens(100)
        return message_processing

class ActionDecorator(MessageProcessing):
    
    def __init__(self, decorator : MessageProcessing, llm_api : LLM_API):
        super(ActionDecorator, self).__init__(decorator)      
        self._llm_api = llm_api

    def get_messages(self) -> MessageStruct:
        message_processing = self._decorator.get_messages()        
        messages = message_processing.get_history().get_messages()
        
        message = 'Your role is an AI bot. Based on the Instruction and the Message plan what is best for the future. Next steps, where to go. What to do. \n'
        message = message + 'Instruction:\n' + message_processing.get_instruction().get_message() + '\n'    
        message = message + 'Message:\n' + messages[-1].message + '\n' 
        
        ai_message = AIMessage(message=message, role="user", class_type="MessageAI", sender="user")
        ai_messages = AIMessages()
        ai_messages.add_message(ai_message)
        
        self._llm_api.set_max_tokens(10)
        reply = self._llm_api.query_text(ai_messages)
        print('--- ---')
        print('Plan: ' + reply)
        print('--- ---')
        m = message_processing.get_instruction()
        m.message = m.message + '\nYour plans for the future:' + reply
        message_processing.set_instruction(m)

        self._llm_api.set_max_tokens(100)
        return message_processing

# ---


if __name__ == "__main__":
    setup_logging("python_server_endpoint")
    import torch

    from LLM_Character.llm_comms.llm_openai import OpenAIComms
    from LLM_Character.llm_comms.llm_local import LocalComms

    logger.info("CUDA found " + str(torch.cuda.is_available()))

    # AI role
    message = AIMessage(message='You play a role. Answer according to your role. You are a pirat. Reply in a short way. Try to find out more about me. ', role="user", class_type="Introduction", sender="user")
    message_manager = MessageStruct(message)    
    message = AIMessage(message='hi', role="assistant", class_type="MessageAI", sender="assistant")
    message_manager.add_message(message)
    
    message_decorator = BaseDecorator(message_manager)    

    model = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    # model_id = "genericgod/GerMerge-em-leo-mistral-v0.2-SLERP"

    # model = OpenAIComms()
    # model_id = "gpt-4o"

    model.init(model_id)
    wrapped_model = LLM_API(model)    
    model.max_tokens = 100

    importance_decorator = ImportanceDecorator(message_decorator, wrapped_model)
    emotion_decorator = EmotionDecorator(importance_decorator, wrapped_model)
    action_decorator = ActionDecorator(emotion_decorator, wrapped_model)

    while True:
        query_introduction = input("Chat: ")
        if query_introduction == "q":
            break        
        
        message = AIMessage(message=query_introduction, role="user", class_type="MessageAI", sender="user")
        message_manager.add_message(message)
        query = action_decorator.get_messages().get_instruction_and_history()
        
        print('--- ---')
        print(query.prints_messages_role())
        print('--- ---')
        
        query_result = wrapped_model.query_text(query)
        print(query_result)
        message = AIMessage(message=query_result, role="assistant", class_type="MessageAI", sender="assistant")
        message_manager.add_message(message)

