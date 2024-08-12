import sys
sys.path.append('../../')

from abc import ABC, abstractmethod

class BaseDispatcher(ABC):
  @abstractmethod
  def handler(self, socket, server, model, data):
    pass
