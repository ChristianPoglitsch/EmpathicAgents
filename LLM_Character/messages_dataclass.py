""" Module providing dataclasses responsible for storing messages. """

import json
from typing import List, Union

class AIMessage:
    """A single message of a chat."""

    def __init__(self, sender:str, message:str, role: str, class_type:str):
        """
        Initializes the AIMessage instance.

        Args:
            message (str): The message sent in the chat.
            role (str): The sender of the message, either `user` or `assistant`.
            kwargs (dict): Includes the field `class_type` to indicate if this message
            is part of the system background for the LLM. (e.g. `MessageAI` or `Introduction`)
        """
        self.message = message
        self.role = role
        self.sender = sender
        self.class_type= class_type 

    def get_message_formatted(self) -> dict[str, str]:
        """
        Formats the message as a dictionary with fields `class_type`, `role`, and `content`.

        Returns:
            dict[str, str]: A dictionary representing the message
            with `class_type`, `role`, and `content`.
        """
        return {
            "sender": self.sender, 
            "content": self.message,
            "role": self.role,
            "class_type": self.class_type,
        }

    def print_message_role(self) -> str:
        """
        Formats the message as a string with the format `[role] content \\n`.
        Returns:
            str: The formatted message string.
        """
        return "[" + self.role + "] " + self.message + "\n"

    def print_message_sender(self) -> str : 
        """
        Formats the message as a string with the format `sender: content \\n`.
        """
        return self.sender + ": " + self.message

    def get_user_message(self) -> str:
        """
        Returns the content of the message if the role is 'user'
        and the message is not part of the system background.
        Returns `None` otherwise.

        Returns:
            str or None: The content of the message if it is
            from the 'user' role and not part of the system background; otherwise, `None`.
        """
        if self.class_type == "MessageAI" and self.role == "user":
            return self.message
        return None

    def get_message(self) -> str: 
        return self.message

    def get_role(self) -> str:
        """
        Returns the role of this message.

        Returns:
            str: The role of the message (e.g., 'user' or 'assistant').
        """
        return self.role

    def get_type(self) -> str:
        """
        Returns the `class_type` of this message,
        indicating if it is part of the system background or not.

        Returns:
            str: The class type of the message (e.g., 'MessageAI' or 'Introduction').
        """
        return self.class_type


class AIMessages:
    """
    Represents the messages of an entire chat.
    """

    def __init__(self):
        self.messages: List[AIMessage] = []

    def add_message(self, message: str, sender:str, role: str, class_type:str):
        """
        Creates an AIMessage instance with the given `message` and `role`.

        Args:
            message (str): The content of the message.
            role (str): The role of the sender (e.g., 'user' or 'assistant').

        Returns:
            AIMessage: The created AIMessage instance.
        """
        self.messages.append(AIMessage(sender, message, role, class_type))

    def get_messages(self) -> List[AIMessage]:
        """
        Retrieves all the messages stored in this chat.

        Returns:
            List[AIMessage]: A list of AIMessage instances representing the chat history.
        """
        return self.messages

    def get_messages_formatted(self) -> List[dict]:
        """
        Represents the messages of this chat as a list of
        dictionaries with fields `class_type`, `role`, and `content`.

        Returns:
            List[dict]: A list of dictionaries representing the formatted messages.
        """
        message_list = []
        for item in self.messages:
            message_list.append(item.get_message_formatted())
        return message_list

    def prints_messages_role(self):
        """
        Represents the messages of this chat as a single string,
        with each message formatted as `[role] content \\n`.

        Returns:
            str: A string containing all the messages formatted.
        """
        m = ""
        for item in self.messages:
            m = m + item.print_message_role()
        return m

    def prints_messages_sender(self):
        """
        Represents the messages of this chat as a single string,
        with each message formatted as `sender : content \\n`.

        Returns:
            str: A string containing all the messages formatted.
        """
        m = ""
        for item in self.messages:
            m = m + item.print_message_sender()
        return m

    def get_user_message(self) -> AIMessage:
        """
        Concatenates all messages with the role 'user' into a single string.
        Returns an `AIMessage` object with the concatenated string as the content of the message.

        Returns:
            AIMessage: An AIMessage instance with the concatenated user messages.
        """
        user_message = ""
        for item in self.messages:
            m = item.get_user_message()
            if m is not None:
                user_message = user_message + m  # QUESTION: no delimter?
        return AIMessage(user_message, "user")

    def write_messages_to_json(self, file_path):
        """
        Writes the formatted messages to a JSON file.

        Args:
            file_path (str): The path to the file where the messages should be saved.
        """
        with open(file_path, "w") as json_file:
            json.dump(self.get_messages_formatted(), json_file, indent=4)
    
    @staticmethod
    def read_messages_from_json(file_path):
        """
        Reads messages from a JSON file and populates a new AIMessages instance.

        Args:
            file_path (str): The path to the JSON file to read from.

        Returns:
            AIMessages: An AIMessages instance populated with the messages read from the file.
        """
        messages_ai = AIMessages()
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            for item in data:
                message_ai = AIMessage(
                    item["content"], item["role"], class_type=item["class_type"]
                )
                messages_ai.add_message(message_ai)
        return messages_ai


    def  __len__(self):
        return  len(self.messages)


if __name__ == "__main__":

    pm = PromptMessage(1, "Hallo Wereld")
    print("JSON ", pm.toJSON())

    print("\n")
    print("--------------------")
    print("\n")
    
    ai_message = AIMessage("Hallo", "user", class_type="MessageAI")
    print("message_formatted: ", ai_message.get_message_formatted())
    print("print_message: ", ai_message.print_message())
    print("get_user_message: ", ai_message.get_user_message())
    print("get_role: ", ai_message.get_role())
    print("get_type: ", ai_message.get_type())

    print("\n")
    print("--------------------")
    print("\n")

    aimessages = AIMessages()
    aimessages.add_message(AIMessage("Hello", "user"))
    aimessages.add_message(AIMessage("Hi", "assistant"))
    aimessages.add_message(AIMessage("How are you?", "user"))

    print("get_messages_formatted: ", aimessages.get_messages_formatted())
    
    file_path = "dialogues/test_messages.json"
    aimessages.write_messages_to_json(file_path)
    print(f"written to {file_path}")

    print("read from JSON: ", AIMessages.read_messages_from_json(file_path).prints_messages())

    print("\n")
    print("--------------------")
    print("\n")
    
    struct_message = {
        "message": "Hello",
        "Trust": "3",
        "Time": "11 AM",
        "Location": "Graz",
        "Emotion": "Neutral",
    }

    serialised_message = json.dumps(struct_message)
    m = AIMessage(serialised_message, "assistant")
    messages_dict = m.get_message_formatted()
    print("serialised_message: ", messages_dict)



    print("\n")
    print("--------------------")
    print("\n")

    aimessages = AIMessages()
    aimessage  = AIMessage("Hello", "user")
    aimessages.add_message(aimessage)
    aimessages.add_message(AIMessage("Hi", "assistant"))
    aimessages.add_message(AIMessage("How are you?", "user"))

    # b = [i.__dict__ for i in aimessages.get_messages()]
    b = aimessages.get_messages_formatted()
    print(b)    
    print("--------------------")

    json_string2 = json.dumps(b)
    print(json_string2)
    print("--------------------")

    d2 = json.loads(json_string2)
    print(d2)
