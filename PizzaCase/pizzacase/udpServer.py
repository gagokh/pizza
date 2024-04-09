import socket
from cryptography.fernet import Fernet

# Laden van de geheime sleutel uit een extern bestand
def load_secret_key():
    """
    Laad de geheime sleutel uit het bestand 'secret_key.txt'.

    Returns:
        bytes: De geladen geheime sleutel.
    """
    with open('secret_key.txt', 'rb') as keyfile:
        return keyfile.read()

# Gebruik de geladen sleutel om gegevens te versleutelen/ontsleutelen
secret_key = load_secret_key()
cipher = Fernet(secret_key)

# Definieer de UDP-serverconfiguratie
UDP_IP = 'localhost'  # Vervang dit door het gewenste IP-adres
UDP_PORT = 1244  # Vervang dit door het gewenste poortnummer

# Maak een UDP-socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

print(f"UDP-server gestart op {UDP_IP}:{UDP_PORT}")

while True:
    # Wacht op inkomende berichten
    data, addr = udp_socket.recvfrom(1024)  # Maximaal 1024 bytes per keer ontvangen

    try:
        decrypted_data = cipher.decrypt(data)
        print(f"Ontvangen bericht van {addr}:")
        print(decrypted_data.decode('utf-8'))
    except Exception as e:
        print(f"Fout bij het verwerken van het bericht van {addr}: {str(e)}")

# Sluit de socket (dit wordt meestal niet bereikt in een servertoepassing)
udp_socket.close()
