from ..communication.tcp_handler import TCPHandler
from ..communication.udp_handler import UDPHandler
from ..communication.http_handler import HTTPHandler

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.init_strategies()
        return cls._instance

    def init_strategies(self):
        """
        Initialise strategies.
        """
        self.strategies = {
            'TCP': TCPHandler('localhost', 1243),  # Pas de host en poort aan
            'UDP': UDPHandler('localhost', 1244),  # Pas de host en poort aan
            'HTTP': HTTPHandler('http://localhost:8080'),  # Pas de URL aan
        }

    def get_strategy(self, communication_method):
        """
        Get the communication strategy based on the specified method.

        Args:
            communication_method (str): the wanted communication method ('TCP', 'UDP' of 'HTTP').

        Returns:
            CommunicationStrategy: The chosen strategy.

        """
        return self.strategies.get(communication_method)
