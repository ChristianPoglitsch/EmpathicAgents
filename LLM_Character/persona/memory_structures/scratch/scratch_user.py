import sys
import datetime
import json
sys.path.append('../../')

from LLM_Character.world.validation_dataclass import  ScratchData
from LLM_Character.util import check_if_file_exists

class ScratchUser: 
    def __init__(self, name, f_saved): 
        # WORLD INFORMATION 
        self.curr_time = None
        self.curr_location = None 

        # REFLECTION VARIABLES
        self.recency_w = 1
        self.relevance_w = 1
        self.importance_w = 1
        self.recency_decay= 0.99
        
        self.act_address = None
        self.act_start_time = None
        self.act_duration = None
        self.act_description = None
        self.act_event = (name, None, None)
        self.chatting_with = None 
        self.chat = None 
        self.chatting_with_buffer = None 
          
        # FIXME: gevallenonderscheid tussen user object en persona object. 
        if check_if_file_exists(f_saved): 
            # If we have a bootstrap file, load that here. 
            scratch_load = json.load(open(f_saved))

            if scratch_load["curr_time"]: 
                self.curr_time = datetime.datetime.strptime(scratch_load["curr_time"],
                                                        "%B %d, %Y, %H:%M:%S")
            else: 
                self.curr_time = None
            
            self.curr_location = scratch_load["curr_location"]
            self.recency_w = scratch_load["recency_w"]
            self.relevance_w = scratch_load["relevance_w"]
            self.importance_w = scratch_load["importance_w"]
            self.recency_decay = scratch_load["recency_decay"]
            # self.importance_trigger_max = scratch_load["importance_trigger_max"]
            # self.importance_trigger_curr = scratch_load["importance_trigger_curr"]
            # self.importance_ele_n = scratch_load["importance_ele_n"]
            # self.thought_count = scratch_load["thought_count"]

            self.act_address = scratch_load["act_address"]
            if scratch_load["act_start_time"]: 
                self.act_start_time = datetime.datetime.strptime(
                                                    scratch_load["act_start_time"],
                                                    "%B %d, %Y, %H:%M:%S")
            else: 
                self.curr_time = None
            self.act_duration = scratch_load["act_duration"]
            self.act_description = scratch_load["act_description"]
            # NOTE ik denk niet dat dit hetzelfde is als een event uit Associative memory, klopt dit? idk, check
            # wnr dit intialised is, als in perceived, dan nu allesinds niet nodig. 
            self.act_event = tuple(scratch_load["act_event"])

            self.chatting_with = scratch_load["chatting_with"]
            self.chat = scratch_load["chat"]
            self.chatting_with_buffer = scratch_load["chatting_with_buffer"]
            if scratch_load["chatting_end_time"]: 
              self.chatting_end_time = datetime.datetime.strptime(
                                                  scratch_load["chatting_end_time"],
                                                  "%B %d, %Y, %H:%M:%S")
            else:
              self.chatting_end_time = None

    @staticmethod
    def save_as(f_saved:str, data:ScratchData):
      scratch = dict() 
      scratch["curr_time"] = data.curr_time.strftime("%B %d, %Y, %H:%M:%S")
      scratch["curr_location"] = data.curr_location

      scratch["recency_w"] = data.recency_w
      scratch["relevance_w"] = data.relevance_w
      scratch["importance_w"] = data.importance_w
      scratch["recency_decay"] = data.recency_decay
    #   scratch["importance_trigger_max"] = data.importance_trigger_max
    #   scratch["importance_trigger_curr"] = data.importance_trigger_curr
    #   scratch["importance_ele_n"] = data.importance_ele_n
    #   scratch["thought_count"] = data.thought_count

      scratch["act_address"] = data.act_address
      scratch["act_start_time"] = (data.act_start_time
                                      .strftime("%B %d, %Y, %H:%M:%S"))
      scratch["act_duration"] = data.act_duration
      scratch["act_description"] = data.act_description
      scratch["act_event"] = data.act_event

      scratch["chatting_with"] = data.chatting_with
      scratch["chat"] = data.chat
      scratch["chatting_with_buffer"] = data.chatting_with_buffer
      if data.chatting_end_time: 
        scratch["chatting_end_time"] = (data.chatting_end_time
                                          .strftime("%B %d, %Y, %H:%M:%S"))
      else: 
        scratch["chatting_end_time"] = None

      with open(f_saved, "w") as outfile:
        json.dump(scratch, outfile, indent=2)     



    def save(self, out_json):
      scratch = dict() 
      scratch["curr_time"] = self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
      scratch["curr_location"] = self.curr_location

      scratch["recency_w"] = self.recency_w
      scratch["relevance_w"] = self.relevance_w
      scratch["importance_w"] = self.importance_w
      scratch["recency_decay"] = self.recency_decay
    #   scratch["importance_trigger_max"] = self.importance_trigger_max
    #   scratch["importance_trigger_curr"] = self.importance_trigger_curr
    #   scratch["importance_ele_n"] = self.importance_ele_n
    #   scratch["thought_count"] = self.thought_count

      scratch["act_address"] = self.act_address
      scratch["act_start_time"] = (self.act_start_time
                                      .strftime("%B %d, %Y, %H:%M:%S"))
      scratch["act_duration"] = self.act_duration
      scratch["act_description"] = self.act_description
      scratch["act_event"] = self.act_event

      scratch["chatting_with"] = self.chatting_with
      scratch["chat"] = self.chat
      scratch["chatting_with_buffer"] = self.chatting_with_buffer
      if self.chatting_end_time: 
        scratch["chatting_end_time"] = (self.chatting_end_time
                                          .strftime("%B %d, %Y, %H:%M:%S"))
      else: 
        scratch["chatting_end_time"] = None

      with open(out_json, "w") as outfile:
        json.dump(scratch, outfile, indent=2) 
    
    # --- SETTERS -----
    def add_new_action(self, 
                       action_address, 
                       action_duration,
                       action_description,
                       action_event,
                       chatting_with, 
                       chat, 
                       chatting_with_buffer,
                       chatting_end_time,
                       act_start_time=None): 
      self.act_address = action_address
      self.act_duration = action_duration
      self.act_description = action_description
      self.act_event = action_event

      self.chatting_with = chatting_with
      self.chat = chat 
      if chatting_with_buffer: 
        self.chatting_with_buffer.update(chatting_with_buffer)
      self.chatting_end_time = chatting_end_time

      self.act_start_time = self.curr_time

    # --- STATE ----

    def act_check_finished(self): 
      if not self.act_address: 
        return True

      x = self.act_start_time
      
      if x.second != 0: 
        x = x.replace(second=0)
        x = (x + datetime.timedelta(minutes=1))
      end_time = (x + datetime.timedelta(minutes=self.act_duration))
      
      # FIXME: why not <= ???, you depend on the while true loop in the reverie.  
      if end_time.strftime("%H:%M:%S") == self.curr_time.strftime("%H:%M:%S"): 
        return True
      return False

    # --- GETTERS -----
    # TODO delete the getters that you dont need. 

    def get_str_curr_date_str(self): 
      return self.curr_time.strftime("%A %B %d")


    def get_curr_event(self):
      if not self.act_address: 
        return (self.name, None, None)
      else: 
        return self.act_event


    def get_curr_event_and_desc(self): 
      if not self.act_address: 
        return (self.name, None, None, None)
      else: 
        return (self.act_event[0], 
                self.act_event[1], 
                self.act_event[2],
                self.act_description)

    def act_summary_str(self):
      start_datetime_str = self.act_start_time.strftime("%A %B %d -- %H:%M %p")
      ret = f"[{start_datetime_str}]\n"
      ret += f"Activity: {self.name} is {self.act_description}\n"
      ret += f"Address: {self.act_address}\n"
      ret += f"Duration in minutes (e.g., x min): {str(self.act_duration)} min\n"
      return ret
