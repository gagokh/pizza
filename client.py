import socket
import ssl
import re

# Constant representing the size of the header for the order message
HEADERSIZE = 10

# Global variable to hold the socket
s = None

# Menu and Toppings options
MENU = {"pizza1", "pizza2", "pizza3", "pizza4", "pizza5"}
TOPPINGS = {"topping1", "topping2", "topping3", "topping4", "topping5"}

# List to store Name, Address, and Postcode
NAW = []

# Function to establish a connection based on the communication method (TCP or HTTPS)
def establish_connection(method):
    global s
    if method == 'TCP':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 1243))
    elif method == 'HTTPS':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 1243))
        # Create an SSL context for secure communication
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # Wrap the socket with SSL
        s = context.wrap_socket(s, server_hostname=socket.gethostname())
    else:
        raise ValueError("Unsupported communication method")

# Function to sanitize input by stripping whitespaces and removing special characters
def sanitize_input(input_string):
    sanitized_string = input_string.strip()
    sanitized_string = re.sub(r'[^a-zA-Z0-9\s,]', '', sanitized_string)
    return sanitized_string

# Function to validate quantity as a positive integer
def validate_quantity(input_string):
    try:
        quantity = int(input_string)
        if quantity <= 0:
            return None
        return quantity
    except ValueError:
        return None

# Function to get the order details from the user
def get_order():
    current_order = {}
    while True:
        print("Wat is je naam?")
        naam = sanitize_input(input())

        print("Wat is je straat?")
        straat = sanitize_input(input())

        print("Wat is je postcode?")
        postcode = sanitize_input(input())

        NAW.append(naam)
        NAW.append(straat)
        NAW.append(postcode)

        while True:
            print(*MENU)
            print("Wat voor pizza wil je bestellen?")
            pizza = sanitize_input(input())
            if pizza in MENU:
                if pizza not in current_order:
                    current_order[pizza] = {}

                while True:
                    print(*TOPPINGS)
                    print(f"Welke topping wil je voor {pizza}?")
                    topping = sanitize_input(input())
                    if topping in TOPPINGS:
                        print(f"Hoeveel {pizza} met topping {topping} wil je bestellen?")
                        quantity = validate_quantity(input())
                        if quantity is None:
                            print("Ongeldige invoer, probeer opnieuw")
                            continue
                        current_order[pizza][topping] = quantity
                        break
                    else:
                        print("Deze topping hebben we niet.")
                        continue
            else:
                print("Deze pizza hebben we niet.")
                continue

            print("Verder nog iets? (ja/nee)")
            choice = sanitize_input(input())
            if choice == "nee":
                return current_order
            elif choice != "ja":
                print("Ongeldige invoer. Bestelling wordt afgerond.")
                return current_order

# Function to send the order details to the server
def send_order(order_dict):
    global s
    # Create a formatted order string
    order_string = "\n".join(NAW) + "\n"
    for pizza, toppings in order_dict.items():
        for topping, quantity in toppings.items():
            order_string += f"{quantity} {pizza} met topping {topping}\n"

    # Add the message header with the length of the order string
    msg = f"{len(order_string):<{HEADERSIZE}}" + order_string

    # Send the order message to the server
    s.send(bytes(msg, "utf-8"))

# Function to output the order details to the console
def output_order(order_dict):
    for pizza, toppings in order_dict.items():
        print(f"{pizza}:")
        for topping, quantity in toppings.items():
            print(f"{quantity} met topping {topping}")
        print()

# Main function that orchestrates the pizza ordering process
def main():
    while True:
        print("Choose communication method: TCP or HTTPS?")
        method = sanitize_input(input())
        if method not in ['TCP', 'HTTPS']:
            print("Invalid method. Please choose TCP or HTTPS.")
            continue

        # Establish a connection based on the chosen method
        establish_connection(method)

        # Get the order details from the user
        order = get_order()
        print("\nUw bestelling:")
        print("\n".join(NAW))
        output_order(order)
        print("Haal uw bestelling af.")

        # Send the order to the server
        send_order(order)

        print("Wilt u nog een bestelling plaatsen? (ja/nee)")
        choice = sanitize_input(input())
        if choice != "ja":
            print("Dank u wel. Tot ziens!")
            break

# Entry point to the script
if __name__ == "__main__":
    main()
