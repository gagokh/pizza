import socket
import re
import requests

from communication_strategy import CommunicationStrategy
from tcp_strategy import TcpCommunication
from udp_strategy import UdpCommunication
from http_strategy import HttpCommunication

# Constanten
HEADERSIZE = 10

# Kies de gewenste communicatiemethode ('TCP', 'UDP' of 'HTTP')
communication_method = 'HTTP'  # Wijzig dit op basis van je behoeften

class CommunicationStrategiesSingleton:
    """
    Singleton-klasse voor communicatiestrategieën.

    Attributes:
        _instance (CommunicationStrategiesSingleton): De instantie van de singleton.

    Methods:
        __new__(cls)
        init_strategies(self)
        get_strategy(self, communication_method)

    """

    _instance = None

    def __new__(cls):
        """
        Maakt een nieuwe instantie van de singleton.

        Returns:
            CommunicationStrategiesSingleton: De singleton-instantie.

        """
        if cls._instance is None:
            cls._instance = super(CommunicationStrategiesSingleton, cls).__new__(cls)
            cls._instance.init_strategies()
        return cls._instance

    def init_strategies(self):
        """
        Initialiseer communicatiestrategieën.
        """
        self.strategies = {
            'TCP': TcpCommunication('localhost', 1243),  # Pas de host en poort aan
            'UDP': UdpCommunication('localhost', 1244),  # Pas de host en poort aan
            'HTTP': HttpCommunication('http://localhost:8080'),  # Pas de URL aan
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

# Gebruik de Singleton om de strategie te verkrijgen
communication_strategies = CommunicationStrategiesSingleton()

# Pizzamenu
pizza_menu = [
    {'name': 'Margherita', 'price': 10.0},
    {'name': 'Pepperoni', 'price': 12.0},
    {'name': 'Vegetariana', 'price': 11.0},
    {'name': 'Hawaii', 'price': 11.0},
    {'name': 'Tuna', 'price': 11.0}
]

# Beschikbare toppings
TOPPINGS = {"Ham", "Kaas", "Tonijn", "Salami", "Ananas"}

# Gebruikersgegevens
NAW = []

class OrderItem:
    """
    Basisklasse voor items in de bestelling.

    Attributes:
        pizza (str): De naam van de pizza.
        topping (str): De toppings voor de pizza.
        quantity (int): De hoeveelheid pizza's.

    Methods:
        __init__(self, pizza, topping, quantity)

    """

    def __init__(self, pizza, topping, quantity):
        """
        Initialiseert een OrderItem.

        Args:
            pizza (str): De naam van de pizza.
            topping (str): De toppings voor de pizza.
            quantity (int): De hoeveelheid pizza's.

        """
        self.pizza = pizza
        self.topping = topping
        self.quantity = quantity

class Pizza(OrderItem):
    """
    Concrete klasse voor pizza-items in de bestelling.

    Methods:
        __init__(self, name, topping, quantity)
        accept(self, visitor)

    """

    def __init__(self, name, topping, quantity):
        """
        Initialiseert een Pizza-item.

        Args:
            name (str): De naam van de pizza.
            topping (str): De toppings voor de pizza.
            quantity (int): De hoeveelheid pizza's.

        """
        super().__init__(name, topping, quantity)

    def accept(self, visitor):
        """
        Accepteer een bezoeker voor verwerking.

        Args:
            visitor (OrderVisitor): De bezoeker die de pizza verwerkt.

        """
        visitor.visit_pizza(self)

class Order(OrderItem):
    """
    Concrete klasse voor de bestelling.

    Attributes:
        items (list): Een lijst met items in de bestelling.

    Methods:
        __init__(self)
        add_item(self, item)
        accept(self, visitor)

    """

    def __init__(self):
        """
        Initialiseert een Order.

        """
        self.items = []

    def add_item(self, item):
        """
        Voeg een item toe aan de bestelling.

        Args:
            item (OrderItem): Het item dat aan de bestelling moet worden toegevoegd.

        """
        self.items.append(item)

    def accept(self, visitor):
        """
        Accepteer een bezoeker voor verwerking.

        Args:
            visitor (OrderVisitor): De bezoeker die de bestelling verwerkt.

        """
        visitor.visit_order(self)

    def __iter__(self):
        """
        Maakt de bestelling iterabel.

        Returns:
            iter: Een iterator voor de items in de bestelling.

        """
        return iter(self.items)

class OrderVisitor:
    """
    Aangepaste Visitor-klasse voor bestellingbewerkingen.

    Methods:
        visit_pizza(self, pizza)
        visit_order(self, order)

    """

    def visit_pizza(self, pizza):
        """
        Bezoek een pizza-item in de bestelling.

        Args:
            pizza (Pizza): Het pizza-item dat wordt bezocht.

        """
        if pizza.topping != "":
            print(f"Verwerk pizza: {pizza.quantity} {pizza.pizza} met toppings: {pizza.topping}")
        else:
            print(f"Verwerk pizza: {pizza.quantity} {pizza.pizza}")

    def visit_order(self, order):
        """
        Bezoek de hele bestelling.

        Args:
            order (Order): De bestelling die wordt bezocht.

        """
        print("Verwerk bestelling:")
        for item in order.items:
            item.accept(self)

def sanitize_input(input_string):
    """
    Sanitize de invoer van de gebruiker door spaties en speciale tekens te verwijderen.

    Args:
        input_string (str): De invoerstring die moet worden schoongemaakt.

    Returns:
        str: De schoongemaakte invoerstring.

    """
    sanitized_string = input_string.strip()
    sanitized_string = re.sub(r'[^a-zA-Z0-9\s,]', '', sanitized_string)
    return sanitized_string

def validate_quantity(input_string):
    """
    Valideer de ingevoerde hoeveelheid door de gebruiker.

    Args:
        input_string (str): De ingevoerde hoeveelheid als een string.

    Returns:
        int or None: De gevalideerde hoeveelheid (als deze geldig is) of None.

    """
    try:
        quantity = int(input_string)
        if quantity <= 0:
            return None
        return quantity
    except ValueError:
        return None

def get_NAW():
    """
    Haal de naam, straat en postcode van de gebruiker op.

    """
    print("Wat is je naam?")
    naam = sanitize_input(input())

    print("Wat is je straat?")
    straat = sanitize_input(input())

    print("Wat is je postcode?")
    postcode = sanitize_input(input())

    NAW.extend([naam, straat, postcode])

def get_pizza():
    """
    Bestel een pizza.

    Returns:
        Pizza: Het bestelde pizzaproduct.

    """
    while True:
        # Toon het pizzamenu
        for pizza in pizza_menu:
            print(f"Naam: {pizza['name']}, Prijs: {pizza['price']} euro")

        # Vraag naar de gewenste pizza
        print("Wat voor pizza wil je bestellen?")
        pizza_name = sanitize_input(input())
        pizza_exists = False

        for menu_item in pizza_menu:
            if pizza_name == menu_item['name']:
                pizza_exists = True
                pizza = menu_item['name']

                # Vraag naar toppings en hoeveelheid
                topping = get_toppings(pizza)
                quantity = get_quantity(pizza, topping)

                return Pizza(pizza, topping, quantity)

        if not pizza_exists:
            print("Deze pizza hebben we niet.")

def get_toppings(pizza):
    """
    Haal toppings op voor een pizza.

    Args:
        pizza (str): De naam van de pizza waarvoor toppings moeten worden gekozen.

    Returns:
        str: Een komma-gescheiden lijst van geselecteerde toppings.

    """
    selected_toppings = set()  # Gebruik een set om dubbele toppings te voorkomen
    while True:
        print(*TOPPINGS)
        print(f"Welke topping wil je voor {pizza}? (Typ 'klaar' om door te gaan)")
        selected_topping = sanitize_input(input())
        if selected_topping == 'klaar':
            break
        elif selected_topping in TOPPINGS:
            selected_toppings.add(selected_topping)

    # Converteer de set naar een komma-gescheiden string
    topping = ', '.join(selected_toppings)
    return topping

def get_quantity(pizza, topping):
    """
    Haal de hoeveelheid te bestellen pizza's op.

    Args:
        pizza (str): De naam van de pizza.
        topping (str): De toppings voor de pizza.

    Returns:
        int: De hoeveelheid pizza's die moeten worden besteld.

    """
    if topping == "":
        print(f"Hoeveel {pizza} wil je bestellen?")
    else:
        print(f"Hoeveel {pizza} met {topping} wil je bestellen?")
    quantity = validate_quantity(input())
    if quantity is None:
        print("Ongeldige invoer, probeer opnieuw")
    return quantity

def remove_pizza(order, pizza_name):
    """
    Verwijder een pizza uit de bestelling.

    Args:
        order (list): De huidige bestelling.
        pizza_name (str): De naam van de pizza die moet worden verwijderd.

    """
    for item in order:
        if isinstance(item, Pizza) and item.pizza == pizza_name:
            order.remove(item)
            print(f"{pizza_name} is verwijderd uit de bestelling.")
            return
    print(f"{pizza_name} is niet in de bestelling.")

def change_toppings(order, pizza_name):
    """
    Wijzig toppings voor een pizza in de bestelling.

    Args:
        order (list): De huidige bestelling.
        pizza_name (str): De naam van de pizza waarvan de toppings moeten worden gewijzigd.

    """
    for item in order:
        if isinstance(item, Pizza) and item.pizza == pizza_name:
            item.topping = get_toppings(pizza_name)
            print(f"Toppings voor {pizza_name} zijn gewijzigd.")
            return
    print(f"{pizza_name} is niet in de bestelling.")

def get_order():
    """
    Haal de bestelling van de gebruiker op.

    Returns:
        list: Een lijst met items in de bestelling.

    """
    current_order = []
    get_NAW()
    while True:
        print("Opties:")
        print("1. Voeg pizza toe")
        print("2. Verwijder pizza")
        print("3. Wijzig toppings")
        print("4. Afronden en bestellen")

        choice = sanitize_input(input())
        if choice == "1":
            pizza_item = get_pizza()
            current_order.append(pizza_item)
        elif choice == "2":
            print("Welke pizza wilt u verwijderen?")
            pizza_name = sanitize_input(input())
            remove_pizza(current_order, pizza_name)
        elif choice == "3":
            print("Van welke pizza wilt u de toppings wijzigen?")
            pizza_name = sanitize_input(input())
            change_toppings(current_order, pizza_name)
        elif choice == "4":
            return current_order
        else:
            print("Ongeldige invoer. Probeer opnieuw.")

def output_order(order_list, visitor):
    """
    Toon de bestelling met behulp van een bezoeker.

    Args:
        order_list (list): Een lijst met items in de bestelling.
        visitor (OrderVisitor): De bezoeker die de bestelling verwerkt.

    """
    for order_item in order_list:
        order_item.accept(visitor)

def calculate_total_price(order_list, pizza_menu):
    """
    Bereken de totale prijs van de bestelling.

    Args:
        order_list (list): Een lijst met items in de bestelling.
        pizza_menu (list): Het pizzamenu met prijsinformatie.

    Returns:
        float: De totale prijs van de bestelling.

    """
    total_price = 0
    for order_item in order_list:
        pizza_name = order_item.pizza
        pizza_price = next(item['price'] for item in pizza_menu if item['name'] == pizza_name)
        quantity = order_item.quantity
        topping_cost = len(order_item.topping.split(', ')) if order_item.topping else 0
        total_price += (pizza_price + topping_cost) * quantity
    return total_price

def construct_and_send_order(order_list, NAW):
    """
    Construeer en verzend de bestelling.

    Args:
        order_list (list): Een lijst met items in de bestelling.
        NAW (list): Een lijst met naam, straat en postcode van de gebruiker.

    """
    order_string = "\n".join(NAW) + "\n"
    for order_item in order_list:
        pizza_name = order_item.pizza
        quantity = order_item.quantity
        topping = order_item.topping
        if topping == "":
            order_string += f"{quantity} {pizza_name}\n"
        else:
            order_string += f"{quantity} {pizza_name} met toppings: {topping}\n"

    # Gebruik de geselecteerde strategie om het bericht naar de server te verzenden
    selected_strategy = communication_strategies.get_strategy(communication_method)
    selected_strategy.send_message(order_string)

def ask_for_another_order():
    """
    Vraag de gebruiker of ze nog een bestelling willen plaatsen.

    Returns:
        bool: True als de gebruiker nog een bestelling wil plaatsen, False anders.

    """
    while True:
        print("Wilt u nog een bestelling plaatsen? (ja/nee)")
        choice = sanitize_input(input())
        if choice == "nee":
            return False
        elif choice == "ja":
            return True
        else:
            print("Ongeldige invoer. Probeer opnieuw.")

def main():
    """
    Hoofdprogramma voor het plaatsen van pizzabestellingen.

    """
    visitor = OrderVisitor()
    while True:
        order = get_order()
        print("Uw bestelling:")
        print("\n".join(NAW))
        output_order(order, visitor)
        total_price = calculate_total_price(order, pizza_menu)
        print(f"Totale prijs: {total_price} euro")
        print("Haal uw bestelling af.")

        # Roep construct_and_send_order aan om de bestelling te verzenden
        construct_and_send_order(order, NAW)

        if not ask_for_another_order():
            break

if __name__ == "__main__":
    main()
