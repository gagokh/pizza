from communication_strategy import CommunicationStrategy
import socket


class TCPHandler(CommunicationStrategy):
    """
    Klasse voor TCP-communicatie.

    Args:
        host (str): Het hostadres waarmee moet worden verbonden.
        port (int): De poort waarmee moet worden verbonden.

    Attributes:
        host (str): Het hostadres waarmee wordt verbonden.
        port (int): De poort waarmee wordt verbonden.

    """


    def __init__(self, host, port):
        self.host = host
        self.port = port


    def send_message(self, message):
        """
        Verzend een bericht via TCP naar de opgegeven host en poort.

        Args:
            message (str): Het bericht dat moet worden verzonden.

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(bytes(message, 'utf-8'))
        s.close()
