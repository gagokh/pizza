from abc import ABC, abstractmethod

class CommunicationStrategy(ABC):
    @abstractmethod
    def send_message(self, message):
        pass
