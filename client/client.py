import re

from common.pattern.composite import Composite
# from common.pattern.singleton import Singleton
from common.pattern.calculate_totalprice_visitor import PriceCalculatorVisitor
from common.pattern.print_order_visitor import PrintOrderVisitor
from common.pattern.singleton import Singleton
from common.pizza import Pizza

NAW = []
pizza_menu = [
    {'name': 'Margherita', 'price': 10.0},
    {'name': 'Pepperoni', 'price': 12.0},
    {'name': 'Vegetariana', 'price': 11.0},
    {'name': 'Hawaii', 'price': 11.0},
    {'name': 'Tuna', 'price': 11.0}
]

TOPPINGS = {"Ham", "Kaas", "Tonijn", "Salami", "Ananas"}

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
                price = menu_item['price']

                # Vraag naar toppings en hoeveelheid
                topping = get_toppings(pizza)
                quantity = get_quantity(pizza, topping)


                # def __init__(self, name, topping, quantity, price):
                return Pizza(pizza, topping, quantity, price)

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


def get_order():
    """
    Haal de bestelling van de gebruiker op.

    Returns:
        list: Een lijst met items in de bestelling.

    """
    current_order = Composite()

    get_NAW()
    while True:
        print("Opties:")
        print("1. Voeg pizza toe")
        print("2. Verwijder pizza")
        print("3. Bekijk bestelling")
        print("4. Afronden en bestellen")

        choice = sanitize_input(input())
        if choice == "1":
            pizza_item = get_pizza()
            current_order.add(pizza_item)
        elif choice == "2":
            print("Welke pizza wilt u verwijderen?")
            pizza_name = sanitize_input(input())
            current_order.find_and_remove_pizza(pizza_name)
        elif choice == "3":
            print("Dit is je huidige bestelling:")
            print_order = PrintOrderVisitor()
            print(print_order.visit_order(current_order))

        elif choice == "4":
            return current_order
        else:
            print("Ongeldige invoer. Probeer opnieuw.")

def construct_and_send_order(order_string):
    """
    Construeer en verzend de bestelling.

    Args:
        order_list (list): Een lijst met items in de bestelling.
        NAW (list): Een lijst met naam, straat en postcode van de gebruiker.

    """
    communication_method = 'HTTP'

    singleton = Singleton()

    # Gebruik de geselecteerde strategie om het bericht naar de server te verzenden
    selected_strategy = singleton.get_strategy(communication_method)
    selected_strategy.send_message(order_string)


def main():


    while True:
        order = get_order()
        price_calculator = PriceCalculatorVisitor()
        total_price = price_calculator.visit_order(order)
        print(f"Totaalprijs van de bestelling: €{total_price:.2f}")

        order_string = "\n".join(NAW) + "\n"
        print_order = PrintOrderVisitor()
        order_string += print_order.visit_order(order)

        print("Uw bestelling:")
        print(order_string)

        print("Haal uw bestelling af.")

        construct_and_send_order(order_string)


if __name__ == "__main__":
    main()
