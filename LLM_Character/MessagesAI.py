import json

class MessageAI():

    def __init__(self, message, role, *args, **kwargs):
        self.message =  message
        self.role = role
        class_type = kwargs.get('class_type', 'MessageAI')
        self.class_type = class_type

    def get_message_formatted(self):
        return {"class_type": self.class_type, "role": self.role, "content": self.message}
    
    def print_message(self):
        return '[' + self.role + '] ' + self.message + '\n'

    def get_user_message(self):
        if self.class_type == "MessageAI" and self.role == 'user':
            return self.message
        return None
    
    def get_role(self):
        return self.role
    
    def get_type(self):
        return self.class_type


class MessageAIStruct(MessageAI):
    
    def __init__(self, message, role, *args, **kwargs):
        self.message = message
        self.role = role
        class_type = kwargs.get('class_type', 'MessageAI')
        self.class_type = class_type
        message_as_string = self.get_message_to_string()
        self.set_message_as_string(message_as_string)
        message_as_json = self.get_message_as_string()
        super().__init__(message_as_string, role, args, kwargs)

    def get_message_formatted(self):
        return {"class_type": self.class_type, "role": self.role, "content": json.dumps(self.message)}

    def get_message_to_string(self):
        return json.dumps(self.message)
    
    def get_message_as_string(self):
        return self.message

    def set_message_as_string(self, message):
        self.message = json.loads(message)

class MessagesAI():

    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        
    def create_message(self, message, role):
        return MessageAI(message, role)

    def get_messages(self):
        return self.messages

    def get_messages_formatted(self):
        message_list = []
        for item in self.messages:
            message_list.append(item.get_message_formatted())
        return message_list

    def prints_messages(self):
        m = ''
        for item in self.messages:
            m = m + item.print_message()
        return m

    def get_user_message(self):
        user_message = ""
        for item in self.messages:
            user_message = user_message + item.get_user_message()
        return MessageAI(user_message, "user")

    def write_messages_to_json(self, file_path):
        with open(file_path, "w") as json_file:
            json.dump(self.get_messages_formatted(), json_file, indent=4)

    def read_messages_from_json(self, file_path):
        messages_ai = MessagesAI()
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            for item in data:
                message_ai = MessageAI(item["content"], item["role"], class_type = item["class_type"])
                messages_ai.add_message(message_ai)
        return messages_ai


struct_message = {"message": "Hello", "Trust": "3", "Time": "11 AM", "Location": "Graz", "Emotion": "Neutral"}
m = MessageAIStruct(struct_message, "assistant")
print(m.get_message_formatted())
