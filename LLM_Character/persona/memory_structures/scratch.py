""" Short term memory """

from datetime import datetime
class Scratch: 
    def __init__(self, f_saved): 
      # PERSONA HYPERPARAMETERS

      # WORLD INFORMATION 
      self.curr_time = None
      self.curr_location = None 

      # THE CORE IDENTITY OF THE PERSONA 
      self.name = None
      self.first_name = None
      self.last_name = None
      self.age = None
      # characterstics of the character
      self.innate = None
      self.learned = None
      self.currently = None
      self.lifestyle = None
      self.living_area = None

      # REFLECTION VARIABLES
      self.recency_w = 1
      self.relevance_w = 1
      self.importance_w = 1

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
    def get_str_curr_date_str(self) -> str:
      return ""

    def get_str_iss(self) -> str:
      return "" 

    def get_str_lifestyle(self) -> str:
      return ""

    def get_str_firstname(self) -> str: 
      return ""

    def get_curr_location(self):
      return {}

    def get_living_area(self):
      return {}

    def get_str_name(self) -> str:
      return ""

    def get_str_daily_plan_req(self) -> str: 
      return ""

    def get_f_daily_schedule_hourly_org(self):
      return self.f_daily_schedule_hourly_org[:]

    def get_f_daily_schedule_hourly_org_index(self, advance=0):
      """
      We get the current index of self.f_daily_schedule_hourly_org. 
      It is otherwise the same as get_f_daily_schedule_index. 

      INPUT
        advance: Integer value of the number minutes we want to look into the 
                 future. This allows us to get the index of a future timeframe.
      OUTPUT 
        an integer value for the current index of f_daily_schedule.
      """
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
