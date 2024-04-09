from cryptography.fernet import Fernet

def generate_secret_key():
    return Fernet.generate_key()

# Genereer een nieuwe geheime sleutel
secret_key = generate_secret_key()

# Bewaar de sleutel veilig (bijvoorbeeld in een configuratiebestand)
with open('secret_key.txt', 'wb') as keyfile:
    keyfile.write(secret_key)
