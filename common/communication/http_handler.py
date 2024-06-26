import requests
from cryptography.fernet import Fernet


def generate_secret_key():
    # Generate the secret key and store it in a file
    with open('secret_key.txt', 'wb') as keyfile:
        keyfile.write(Fernet.generate_key())


def load_secret_key():
    """
    Load the secret key 'secret_key.txt'.

    :return: Return the secret key as bytes.
    """
    # Check if the key file exists, otherwise generate a new key
    try:
        with open('secret_key.txt', 'rb') as keyfile:
            return keyfile.read()
    except FileNotFoundError:
        generate_secret_key()
        with open('secret_key.txt', 'rb') as keyfile:
            return keyfile.read()

# Use the secret key
secret_key = load_secret_key()


class HTTPHandler:
    """
    Klasse voor HTTP-communicatie.

    Args:
        url (str): De URL van de server waarmee moet worden gecommuniceerd.

    Attributes:
        url (str): De URL van de server waarmee wordt gecommuniceerd.
        key (bytes): De geheime sleutel voor gegevensversleuteling.
        cipher (Fernet): Het Fernet-cijferobject voor versleuteling.

    """

    def __init__(self, url):
        self.url = url
        self.key = load_secret_key()
        self.cipher = Fernet(self.key)

    def send_message(self, message):
        """
        Verzend een versleuteld bericht naar de server via HTTP.

        Args:
            message (str): Het bericht dat moet worden verzonden.

        """
        # Versleutel het bericht
        encrypted_message = self.cipher.encrypt(message.encode('utf-8'))

        # Verzend het versleutelde bericht naar de server
        response = requests.post(self.url, data=encrypted_message)

        if response.status_code == 200:
            print('HTTP-verzoek succesvol verzonden')
        else:
            print(f'HTTP-verzoek mislukt met statuscode: {response.status_code}')
