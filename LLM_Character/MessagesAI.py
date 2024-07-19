import json
from typing import List

class AIMessage():
    """
        A single message of a chat.
    """
    def __init__(self, message:str, role:str, **kwargs:dict):
        """
        message : the message sent in the chat. 
        role : the sender of the message, the assistent or the user. (User or MessageAI)
        kwargs : includes the field `classtype` in order to indicate if this message is part of the system background for the LLM. (MessageAI or Introduction)
        """
        self.message =  message
        self.role = role
        class_type = kwargs.get('class_type', 'MessageAI')
        self.class_type = class_type

    def get_message_formatted(self) -> dict[str, str] : 
        """
        The message is formatted as a json with fields `class_type`, `role` and `content`.
        """
        return {"class_type": self.class_type, "role": self.role, "content": self.message}
    
    def print_message(self) -> str:
        """
        This message is formatted as [`role`] `content` `\\n`
        """
        return '[' + self.role + '] ' + self.message + '\n'

    def get_user_message(self) -> str:
        """
        Returns `None` if the role of this message is not `user` or if the message is part of the system background for the LLM. 
        Otherwise, the content of the message is returned. 
        """ 
        if self.class_type == "MessageAI" and self.role == 'user':
            return self.message
        return None
    
    def get_role(self) -> str:
        """
        Returns the role of this message.
        """
        return self.role
    
    def get_type(self) -> str:
        """
        Returns the `class_type` of this message, i.e. if this message is part of the system background or not. 
        """
        return self.class_type


class AIMessages():
    """
        AIMessages represents the messages of an entire chat.
    """
    def __init__(self):
        self.messages: List[AIMessage] = []

    def add_message(self, message:AIMessage):
        """
        Add an AIMessage instance to the chat history.
        """
        self.messages.append(message)
        
    def create_message(self, message:str, role:str) -> AIMessage:
        """
        Create an AIMessage instance with the given `message` and `role`
        """
        return AIMessage(message, role)

    def get_messages(self) -> List[AIMessage]:
        """
        Retrieve all the messages stored in this chat.
        """
        return self.messages

    def get_messages_formatted(self) -> List[dict]:
        """
        The messages of this chat are represented as a list `Json` with fields `class_type`, `role` and `content`.
        """
        message_list = []
        for item in self.messages:
            message_list.append(item.get_message_formatted())
        return message_list

    def prints_messages(self):
        """
        The messages of this chat are represented as a string of the format `[role] content \\n`
        """
        m = ''
        for item in self.messages:
            m = m + item.print_message()
        return m

    def get_user_message(self) -> AIMessage:
        """
        The messages with the role `user` of this chat are represented as one single string concatenated.
        Returns an `AIMessage` object with the concatenated string as content of the message.
        """
        user_message = ""
        for item in self.messages:
            m = item.get_user_message()
            if m != None:
                user_message = user_message + m   #QUESTION: no delimter? 
        return AIMessage(user_message, "user")

    # TODO:
    def write_messages_to_json(self, file_path):
        """
        
        """
        with open(file_path, "w") as json_file:
            json.dump(self.get_messages_formatted(), json_file, indent=4)

    # TODO:
    def read_messages_from_json(self, file_path):
        """
        
        """
        messages_ai = AIMessage()
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            for item in data:
                message_ai = AIMessage(item["content"], item["role"], class_type = item["class_type"])
                messages_ai.add_message(message_ai)
        return messages_ai

if __name__ == "__main__":
    struct_message = {"message": "Hello", "Trust": "3", "Time": "11 AM", "Location": "Graz", "Emotion": "Neutral"}
    serialised_message = json.dumps(struct_message)
    m = AIMessage(serialised_message, "assistant")
    mdict = m.get_message_formatted()
    print(json.loads(mdict))