from dataclass import AIMessage, AIMessages
from huggingface import HuggingFace

def summary(model:HuggingFace): 
  """
  Summary of messages
  """
   
  messages = AIMessages()
  messages = messages.read_messages_from_json("dialogues/messages.json")
  
  user_message = messages.get_user_message()
  message = AIMessage("Summerize the chat: " + user_message.get_user_message(), "user")
  messages = AIMessages()
  messages.add_message(message)
  messages = model.query(messages)
