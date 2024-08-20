from incoming_messages import *
from outgoing_messages import *

incoming_message_types = [
                        PromptMessage, 
                        MoveMessage, 
                        UpdateMessage,
                        StartMessage,]

outgoing_message_types = [StartSavedGamesMessage,
                          PromptReponseMessage,]


error_message_types = []