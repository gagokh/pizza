from client.communication.tcp_handler import TCPHandler
from client.communication.udp_handler import UDPHandler
from client.communication.http_handler import HTTPHandler


# import TCPHandler
# import UDPHandler
# import HTTPHandler

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.init_strategies()
        return cls._instance

    def init_strategies(self):
        """
        Initialiseer communicatiestrategieën.
        """
        self.strategies = {
            'TCP': TCPHandler('localhost', 1243),  # Pas de host en poort aan
            'UDP': UDPHandler('localhost', 1244),  # Pas de host en poort aan
            'HTTP': HTTPHandler('http://localhost:8080'),  # Pas de URL aan
        }

    def get_strategy(self, communication_method):
        """
        Haal de communicatiestrategie op op basis van de opgegeven methode.

        Args:
            communication_method (str): De gewenste communicatiemethode ('TCP', 'UDP' of 'HTTP').

        Returns:
            CommunicationStrategy: De gekozen communicatiestrategie.

        """
        return self.strategies.get(communication_method)
