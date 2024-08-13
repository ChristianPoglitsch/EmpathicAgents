import json
import datetime
from typing import Optional, Dict, Any

class BaseScratch:
    def __init__(self, name: str, f_saved: str):
        self.name = name
        self.curr_time = None
        self.curr_location = None
        self.recency_w = 1
        self.relevance_w = 1
        self.importance_w = 1
        self.recency_decay = 0.99
        self.act_address = None
        self.act_start_time = None
        self.act_duration = None
        self.act_description = None
        self.act_event = (self.name, None, None)
        self.chatting_with = None
        self.chat = None
        self.chatting_with_buffer = None
        self.chatting_end_time = None

        if check_if_file_exists(f_saved):
            self.load(f_saved)

    def load(self, f_saved: str):
        with open(f_saved, 'r') as file:
            data = json.load(file)
            self.curr_time = datetime.datetime.strptime(data.get("curr_time", "January 01, 0001, 00:00:00"), "%B %d, %Y, %H:%M:%S")
            self.curr_location = data.get("curr_location")
            self.recency_w = data.get("recency_w", 1)
            self.relevance_w = data.get("relevance_w", 1)
            self.importance_w = data.get("importance_w", 1)
            self.recency_decay = data.get("recency_decay", 0.99)
            self.act_address = data.get("act_address")
            self.act_start_time = datetime.datetime.strptime(data.get("act_start_time", "January 01, 0001, 00:00:00"), "%B %d, %Y, %H:%M:%S")
            self.act_duration = data.get("act_duration")
            self.act_description = data.get("act_description")
            self.act_event = tuple(data.get("act_event", (self.name, None, None)))
            self.chatting_with = data.get("chatting_with")
            self.chat = data.get("chat")
            self.chatting_with_buffer = data.get("chatting_with_buffer")
            self.chatting_end_time = datetime.datetime.strptime(data.get("chatting_end_time", "January 01, 0001, 00:00:00"), "%B %d, %Y, %H:%M:%S")

    def save(self, out_json: str):
        data = {
            "curr_time": self.curr_time.strftime("%B %d, %Y, %H:%M:%S"),
            "curr_location": self.curr_location,
            "recency_w": self.recency_w,
            "relevance_w": self.relevance_w,
            "importance_w": self.importance_w,
            "recency_decay": self.recency_decay,
            "act_address": self.act_address,
            "act_start_time": self.act_start_time.strftime("%B %d, %Y, %H:%M:%S"),
            "act_duration": self.act_duration,
            "act_description": self.act_description,
            "act_event": self.act_event,
            "chatting_with": self.chatting_with,
            "chat": self.chat,
            "chatting_with_buffer": self.chatting_with_buffer,
            "chatting_end_time": self.chatting_end_time.strftime("%B %d, %Y, %H:%M:%S") if self.chatting_end_time else None
        }
        with open(out_json, "w") as outfile:
            json.dump(data, outfile, indent=2)
