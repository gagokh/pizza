from flask import Flask, request, render_template_string
from cryptography.fernet import Fernet

app = Flask(__name__)

# Een lijst om de ontvangen bestellingen bij te houden
orders = []

# Laden van de geheime sleutel uit een extern bestand
def load_secret_key():
    """
    Laad de geheime sleutel uit een extern bestand.

    Returns:
        bytes: De geheime sleutel als bytes.
    """
    with open('../client/secret_key.txt', 'rb') as keyfile:
        return keyfile.read()

# Gebruik de geladen sleutel om gegevens te versleutelen/ontsleutelen
secret_key = load_secret_key()

# Create a cipher object with the same key used for encryption
key = secret_key  # Replace with the actual key used for encryption
cipher = Fernet(key)

@app.route('/', methods=['POST', 'GET'])
def receive_order():
    """
    Ontvang bestellingen via HTTP POST-verzoeken en geef ze weer op een webpagina.

    Returns:
        str: Een HTML-pagina met de ontvangen bestellingen.
    """
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        # Decrypt the encrypted data
        decrypted_data = cipher.decrypt(data.encode('utf-8')).decode('utf-8')

        # Verwerk de ontvangen bestelling hier
        orders.append(decrypted_data)

    # HTML-sjabloon om de bestellingen weer te geven
    order_list = "<ul>"
    for order in orders:
        order_list += f"<li>{order}</li>"
    order_list += "</ul>"

    # Weergeef de bestellingen in de browser
    return render_template_string(f'<html><body><h1>Bestellingen</h1>{order_list}</body></html>')


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
