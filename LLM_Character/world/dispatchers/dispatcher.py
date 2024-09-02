import sys
from abc import ABC, abstractmethod

sys.path.append("../../")


class BaseDispatcher(ABC):
    @abstractmethod
    def handler(self, socket, server, model, data):
        pass
