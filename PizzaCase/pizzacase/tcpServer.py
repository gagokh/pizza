import socket
import time

HEADERSIZE = 10

class OrderProcessor:
    """
    Singleton-klasse voor het verwerken van bestellingen via een TCP-socket.
    """

    _instance = None

    def __new__(cls):
        """
        Creeër een nieuwe instantie van de OrderProcessor-klasse als deze nog niet bestaat.

        Returns:
            OrderProcessor: Een instantie van de OrderProcessor-klasse.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def process_orders(self):
        """
        Luister naar inkomende bestellingen via een TCP-socket en verwerk deze.

        Deze methode blijft luisteren naar inkomende bestellingen en geeft de ontvangen bestellingen en de
        tijdstempel weer.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1243))
        s.listen(5)

        print("Wachten op een verbinding...")
        clientsocket, address = s.accept()
        print(f"Verbinding van {address} is tot stand gebracht.")

        while True:
            full_msg = b''
            new_msg = True
            while True:
                msg = clientsocket.recv(16)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE].decode("utf-8"))
                    new_msg = False

                full_msg += msg

                if len(full_msg) - HEADERSIZE == msglen:
                    order_string = full_msg[HEADERSIZE:].decode('utf-8')
                    print("Ontvangen bestelling:")
                    print(order_string)
                    break

            # Aanvullende code om de tijd en datum weer te geven
            order_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print("Bestellingstijd:", order_time)

            time.sleep(2)

# Gebruik
if __name__ == "__main__":
    order_processor = OrderProcessor()
    order_processor.process_orders()
