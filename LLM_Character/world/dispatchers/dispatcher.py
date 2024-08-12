import sys
sys.path.append('../../')

from abc import ABC, abstractmethod

class BaseDispatcher(ABC):
  @abstractmethod
  def handler(self, data, socket, personas):
    pass
