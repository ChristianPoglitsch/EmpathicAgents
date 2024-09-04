from abc import ABC, abstractmethod


class CommMedium(ABC):
    @abstractmethod
    def read_received_data():
        """
        A Non blocking reading method which reads
        incoming data from the communication medium.
        """
        pass

    @abstractmethod
    def send_data():
        """
        A Non blocking sending method which sends
        outgoing data to the communication medium.
        """
        pass
