""" Short term memory """

import json
import datetime
from typing import Tuple, Union 

from LLM_Character.messages_dataclass import AIMessages
from LLM_Character.world.validation_dataclass import  PersonaScratchData
from LLM_Character.util import check_if_file_exists

# FIXME: curr_location and living_area moeten bepaalde formaten hebben, 
# ze moeten een dicionary zijn met keys world, sector, arena en gameobject indien beschikbaar.

class PersonaScratch: 
    def __init__(self, name, f_saved): 
      # WORLD INFORMATION 
      self.curr_time = None
      self.curr_location = None 

      # THE CORE IDENTITY OF THE PERSONA 
      self.name = name
      self.first_name = None
      self.last_name = None
      self.age = None
      self.innate = None
      self.learned = None
      self.currently = None
      self.lifestyle = None
      self.living_area = None

      # RETRIEVE VARIABLES
      self.recency_w = 1
      self.relevance_w = 1
      self.importance_w = 1
      self.recency_decay= 0.99
      
      # REFLECTION VARIABLES
      self.importance_trigger_max = 150
      self.importance_trigger_curr = self.importance_trigger_max
      self.importance_ele_n = 0 
      # self.thought_count = 5
      
      # PERSONA PLANNING 
      self.daily_req = []
      self.f_daily_schedule = []
      self.f_daily_schedule_hourly_org = []

      # CURR ACTION
      self.act_address = None
      self.act_start_time = None
      self.act_duration = None
      self.act_description = None
      self.act_event = (self.name, None, None)

      self.chatting_with = None 
      self.chat = AIMessages() 
      self.chatting_with_buffer = dict() 
      self.chatting_end_time = None     

      self.load(f_saved)             

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
    def get_f_daily_schedule_index(self, advance=0):
      # We first calculate teh number of minutes elapsed today. 
      today_min_elapsed = 0
      today_min_elapsed += self.curr_time.hour * 60
      today_min_elapsed += self.curr_time.minute
      today_min_elapsed += advance

      x = 0
      for task, duration in self.f_daily_schedule: 
        x += duration
      x = 0
      for task, duration in self.f_daily_schedule_hourly_org: 
        x += duration

      # We then calculate the current index based on that. 
      curr_index = 0
      elapsed = 0
      for task, duration in self.f_daily_schedule: 
        elapsed += duration
        if elapsed > today_min_elapsed: 
          return curr_index
        curr_index += 1

      return curr_index

    def get_curr_event_and_desc(self) -> Tuple[str, Union[str, None], Union[str, None], Union[str, None]]: 
      if not self.act_address: 
        return (self.name, None, None, None)
      else: 
        return (self.act_event[0], 
                self.act_event[1], 
                self.act_event[2],
                self.act_description)

    def get_f_daily_schedule_hourly_org(self, advance=0):
      return self.f_daily_schedule_hourly_org

    def get_f_daily_schedule_hourly_org_index(self, advance=0):
      # We first calculate teh number of minutes elapsed today. 
      today_min_elapsed = 0
      today_min_elapsed += self.curr_time.hour * 60
      today_min_elapsed += self.curr_time.minute
      today_min_elapsed += advance
      # We then calculate the current index based on that. 
      curr_index = 0
      elapsed = 0
      for task, duration in self.f_daily_schedule_hourly_org: 
        elapsed += duration
        if elapsed > today_min_elapsed: 
          return curr_index
        curr_index += 1
      return curr_index
    def get_str_curr_date_str(self) -> str:
      return ""

    def get_str_iss(self) -> str:
      commonset = ""
      commonset += f"Name: {self.name}\n"
      commonset += f"Age: {self.age}\n"
      commonset += f"Innate traits: {self.innate}\n"
      commonset += f"Learned traits: {self.learned}\n"
      commonset += f"Currently: {self.currently}\n"
      commonset += f"Lifestyle: {self.lifestyle}\n"
      commonset += f"Daily plan requirement: {self.daily_plan_req}\n"
      commonset += f"Current Date: {self.curr_time.strftime('%A %B %d')}\n"
      return commonset

    def get_str_name(self): 
      return self.name


    def get_str_firstname(self): 
      return self.first_name


    def get_str_lastname(self): 
      return self.last_name


    def get_str_age(self): 
      return str(self.age)


    def get_str_innate(self): 
      return self.innate


    def get_str_learned(self): 
      return self.learned


    def get_str_currently(self): 
      return self.currently


    def get_str_lifestyle(self): 
      return self.lifestyle


    def get_curr_location(self):
      return self.curr_location

    def get_living_area(self):
      return self.living_area

    def get_str_daily_plan_req(self): 
      return self.daily_plan_req


    def get_str_curr_date_str(self): 
      return self.curr_time.strftime("%A %B %d")


    def get_curr_event(self):
      if not self.act_address: 
        return (self.name, None, None)
      else: 
        return self.act_event

    def act_summary_str(self):
      start_datetime_str = self.act_start_time.strftime("%A %B %d -- %H:%M %p")
      ret = f"[{start_datetime_str}]\n"
      ret += f"Activity: {self.name} is {self.act_description}\n"
      ret += f"Address: {self.act_address}\n"
      ret += f"Duration in minutes (e.g., x min): {str(self.act_duration)} min\n"
      return ret


    def get_str_daily_schedule_summary(self): 
      ret = ""
      curr_min_sum = 0
      for row in self.f_daily_schedule: 
        curr_min_sum += row[1]
        hour = int(curr_min_sum/60)
        minute = curr_min_sum%60
        ret += f"{hour:02}:{minute:02} || {row[0]}\n"
      return ret


    def get_str_daily_schedule_hourly_org_summary(self): 
      ret = ""
      curr_min_sum = 0
      for row in self.f_daily_schedule_hourly_org: 
        curr_min_sum += row[1]
        hour = int(curr_min_sum/60)
        minute = curr_min_sum%60
        ret += f"{hour:02}:{minute:02} || {row[0]}\n"
      return ret

    # LOADING AND SAVING 

    @staticmethod
    def save_as(f_saved:str, data:PersonaScratchData):
      scratch = dict() 
      scratch["curr_time"] = data.curr_time.strftime("%B %d, %Y, %H:%M:%S")
      scratch["curr_location"] = data.curr_location
      scratch["daily_plan_req"] = data.daily_plan_req

      scratch["name"] = data.name
      scratch["first_name"] = data.first_name
      scratch["last_name"] = data.last_name
      scratch["age"] = data.age
      scratch["innate"] = data.innate
      scratch["learned"] = data.learned
      scratch["currently"] = data.currently
      scratch["lifestyle"] = data.lifestyle
      scratch["living_area"] = data.living_area

      # scratch["concept_forget"] = data.concept_forget
      # scratch["daily_reflection_time"] = data.daily_reflection_time
      # scratch["daily_reflection_size"] = data.daily_reflection_size
      # scratch["overlap_reflect_th"] = data.overlap_reflect_th
      # scratch["kw_strg_event_reflect_th"] = data.kw_strg_event_reflect_th
      # scratch["kw_strg_thought_reflect_th"] = data.kw_strg_thought_reflect_th

      scratch["recency_w"] = data.recency_w
      scratch["relevance_w"] = data.relevance_w
      scratch["importance_w"] = data.importance_w
      scratch["recency_decay"] = data.recency_decay
      scratch["importance_trigger_max"] = data.importance_trigger_max
      scratch["importance_trigger_curr"] = data.importance_trigger_curr
      scratch["importance_ele_n"] = data.importance_ele_n
      scratch["thought_count"] = data.thought_count

      scratch["daily_req"] = data.daily_req
      scratch["f_daily_schedule"] = data.f_daily_schedule
      scratch["f_daily_schedule_hourly_org"] = data.f_daily_schedule_hourly_org

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

    def load(self, f_saved:str):
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
            self.daily_plan_req = scratch_load["daily_plan_req"]

            self.name = scratch_load["name"]
            self.first_name = scratch_load["first_name"]
            self.last_name = scratch_load["last_name"]
            self.age = scratch_load["age"]
            self.innate = scratch_load["innate"]
            self.learned = scratch_load["learned"]
            self.currently = scratch_load["currently"]
            self.lifestyle = scratch_load["lifestyle"]
            self.living_area = scratch_load["living_area"]

            # NOTE maybe needed, dont know yet where it they are used; 
            # self.concept_forget = scratch_load["concept_forget"]
            # self.daily_reflection_time = scratch_load["daily_reflection_time"]
            # self.daily_reflection_size = scratch_load["daily_reflection_size"]
            # self.overlap_reflect_th = scratch_load["overlap_reflect_th"]
            # self.kw_strg_event_reflect_th = scratch_load["kw_strg_event_reflect_th"]
            # self.kw_strg_thought_reflect_th = scratch_load["kw_strg_thought_reflect_th"]

            self.recency_w = scratch_load["recency_w"]
            self.relevance_w = scratch_load["relevance_w"]
            self.importance_w = scratch_load["importance_w"]
            self.recency_decay = scratch_load["recency_decay"]
            # self.importance_trigger_max = scratch_load["importance_trigger_max"]
            # self.importance_trigger_curr = scratch_load["importance_trigger_curr"]
            # self.importance_ele_n = scratch_load["importance_ele_n"]
            # self.thought_count = scratch_load["thought_count"]

            self.daily_req = scratch_load["daily_req"]
            self.f_daily_schedule = scratch_load["f_daily_schedule"]
            self.f_daily_schedule_hourly_org = scratch_load["f_daily_schedule_hourly_org"]

            self.act_address = scratch_load["act_address"]
            if scratch_load["act_start_time"]: 
              self.act_start_time = datetime.datetime.strptime(
                                                    scratch_load["act_start_time"],
                                                    "%B %d, %Y, %H:%M:%S")
            else: 
              self.act_start_time = None
            self.act_duration = scratch_load["act_duration"]
            self.act_description = scratch_load["act_description"]
            # NOTE ik denk niet dat dit hetzelfde is als een event uit Associative memory, klopt dit? idk, check
            # wnr dit intialised is, als in perceived, dan nu allesinds niet nodig. 
            self.act_event = tuple(scratch_load["act_event"])

            # self.chatting_with = scratch_load["chatting_with"]
            # self.chat = scratch_load["chat"]
            # self.chatting_with_buffer = scratch_load["chatting_with_buffer"]
            # if scratch_load["chatting_end_time"]: 
            #   self.chatting_end_time = datetime.datetime.strptime(
            #                                       scratch_load["chatting_end_time"],
            #                                       "%B %d, %Y, %H:%M:%S")
            # else:
            #   self.chatting_end_time = None

    def save(self, out_json):
      scratch = dict() 
      scratch["curr_time"] = self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
      scratch["curr_location"] = self.curr_location
      scratch["daily_plan_req"] = self.daily_plan_req

      scratch["name"] = self.name
      scratch["first_name"] = self.first_name
      scratch["last_name"] = self.last_name
      scratch["age"] = self.age
      scratch["innate"] = self.innate
      scratch["learned"] = self.learned
      scratch["currently"] = self.currently
      scratch["lifestyle"] = self.lifestyle
      scratch["living_area"] = self.living_area

      # scratch["concept_forget"] = self.concept_forget
      # scratch["daily_reflection_time"] = self.daily_reflection_time
      # scratch["daily_reflection_size"] = self.daily_reflection_size
      # scratch["overlap_reflect_th"] = self.overlap_reflect_th
      # scratch["kw_strg_event_reflect_th"] = self.kw_strg_event_reflect_th
      # scratch["kw_strg_thought_reflect_th"] = self.kw_strg_thought_reflect_th

      scratch["recency_w"] = self.recency_w
      scratch["relevance_w"] = self.relevance_w
      scratch["importance_w"] = self.importance_w
      scratch["recency_decay"] = self.recency_decay
      scratch["importance_trigger_max"] = self.importance_trigger_max
      scratch["importance_trigger_curr"] = self.importance_trigger_curr
      scratch["importance_ele_n"] = self.importance_ele_n
      scratch["thought_count"] = self.thought_count

      scratch["daily_req"] = self.daily_req
      scratch["f_daily_schedule"] = self.f_daily_schedule
      scratch["f_daily_schedule_hourly_org"] = self.f_daily_schedule_hourly_org

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