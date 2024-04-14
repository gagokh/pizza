import socket
from cryptography.fernet import Fernet

def generate_secret_key():
    # Genereer een nieuwe geheime sleutel
    # Bewaar de sleutel veilig (bijvoorbeeld in een configuratiebestand)
    with open('secret_key.txt', 'wb') as keyfile:
        keyfile.write(Fernet.generate_key())


def load_secret_key():
    """
    Laad de geheime sleutel uit het bestand 'secret_key.txt'.

    :return: De geheime sleutel als bytes.
    """
    try:
        with open('secret_key.txt', 'rb') as keyfile:
            return keyfile.read()
    except FileNotFoundError:
        generate_secret_key()
        with open('secret_key.txt', 'rb') as keyfile:
            return keyfile.read()




# Gebruik de geladen sleutel om gegevens te versleutelen/ontsleutelen
secret_key = load_secret_key()

class UDPHandler:
    """
    Een concrete implementatie van CommunicationStrategy voor UDP-communicatie.

    Deze klasse maakt gebruik van het UDP-protocol om versleutelde berichten naar een opgegeven host en poort te verzenden.
    De berichten worden versleuteld met behulp van een geheime sleutel die uit een bestand 'secret_key.txt' wordt geladen.

    Args:
        host (str): De host waarnaar het bericht moet worden verzonden.
        port (int): De poort waarnaar het bericht moet worden verzonden.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.key = load_secret_key()
        self.cipher = Fernet(self.key)

    def send_message(self, message):
        """
        Verzend een versleuteld bericht via UDP naar de opgegeven host en poort.

        Args:
            message (str): Het bericht dat moet worden verzonden.
        """
        encrypted_message = self.cipher.encrypt(message.encode('utf-8'))
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(encrypted_message, (self.host, self.port))
        udp_socket.close()

