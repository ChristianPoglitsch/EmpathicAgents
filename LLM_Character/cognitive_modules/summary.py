from MessagesAI import MessagesAI, MessageAI

def summary(model): 
  """
  Summary of messages
  """
   
  messages = MessagesAI()
  messages = messages.read_messages_from_json("messages.json")
  
  user_message = messages.get_user_message()
  message = MessageAI("Summerize the chat: " + user_message.get_user_message(), "user")
  messages = MessagesAI()
  messages.add_message(message)
  messages = model.Query(messages)
