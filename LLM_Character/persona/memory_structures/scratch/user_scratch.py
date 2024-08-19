import json
from datetime import datetime
from typing import Optional, Dict, Any

from LLM_Character.messages_dataclass import AIMessages
from LLM_Character.util import check_if_file_exists


class UserScratch:
    def __init__(self, name: str):
        self.name = name
        self.chat = AIMessages()
        self.start_time_chatting = None 
