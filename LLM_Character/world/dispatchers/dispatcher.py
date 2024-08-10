from abc import ABC, abstractmethod

class BaseDispatcher(ABC):
  @abstractmethod
  def handler(self, data):
    pass
