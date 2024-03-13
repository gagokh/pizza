import socket
import ssl
import time

HEADERSIZE = 10

class OrderProcessor:
    def __init__(self, communication_method='TCP'):
        self.communication_method = communication_method
        self.socket = None

    def set_communication_method(self, method):
        self.communication_method = method

    def create_socket(self):
        if self.communication_method == 'TCP':
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.communication_method == 'HTTPS':
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            return context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_side=True)
        else:
            raise ValueError("Unsupported communication method")

    def process_orders(self):
        s = self.create_socket()
        s.bind((socket.gethostname(), 1243))

        s.listen(5)
        print("Waiting for a connection...")

        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")

         # Wrap the socket with SSL if using HTTPS
        if self.communication_method == 'HTTPS':
          context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
          clientsocket = context.wrap_socket(clientsocket, server_side=True)  

        while True:
            full_msg = b''
            new_msg = True

            # Receive data in chunks until a complete message is received
            while True:
                msg = clientsocket.recv(16)

                if not msg:
                    break  # No more data is received, so break out of the loop

                if new_msg:
                    # Extract the length of the message from the header
                    try:
                        msglen = int(msg[:HEADERSIZE].decode("utf-8"))
                    except ValueError:
                        print("Invalid header format received. Skipping message.")
                        break  # Skip this message if the header cannot be decoded as an integer
                    new_msg = False

                # Append the received data to the full message
                full_msg += msg

                # Check if the full message has been received
                if len(full_msg) - HEADERSIZE == msglen:
                    # Extract the order string from the full message
                    order_string = full_msg[HEADERSIZE:].decode('utf-8')
                    print("Order received:")
                    print(order_string)

                    # Additional code to display the time and date
                    order_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    print("Order time:", order_time)

                    # Simulate processing time by sleeping for 2 seconds
                    time.sleep(2)
                    break  # Exit the inner loop after processing the order

# Usage
if __name__ == "__main__":
    # Create an instance of the OrderProcessor class with TCP as the initial communication method
    order_processor = OrderProcessor(communication_method='TCP')

    # Start processing orders
    order_processor.process_orders()
