""" Short term memory """

class Scratch: 
    def __init__(self, f_saved): 
      # PERSONA HYPERPARAMETERS

      # WORLD INFORMATION 
      self.curr_time = None 
      self.curr_location = None 
      
      # THE CORE IDENTITY OF THE PERSONA 
      # NOTE: this is hard coded, it is information that is not changing during the whole simulation.  
      self.name = None
      self.first_name = None
      self.last_name = None
      self.age = None
      # innate characterstics of the character
      self.innate = None
      # some learned characteristics of the character
      self.learned = None
      # ...
      self.currently = None
      # ...
      self.lifestyle = None
      # where does the character live, his domicile address. 
      self.living_area = None

      # REFLECTION VARIABLES

      # PERSONA PLANNING 
      self.daily_req = []
      self.f_daily_schedule = []
      self.f_daily_schedule_hourly_org = []

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

