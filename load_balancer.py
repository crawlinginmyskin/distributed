import socket
import threading

# Server addresses and ports
servers = [
    ('localhost', 3234),  # Server 1
    ('localhost', 3235)   # Server 2
]

# Global variable for tracking the server index
server_index = 0

# Lock for synchronizing access to the server index
server_index_lock = threading.Lock()


class LoadBalancerThread(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        global server_index

        with server_index_lock:
            current_server_index = server_index
            server_index = (server_index + 1) % len(servers)

        server_address, server_port = servers[current_server_index]

        # Connect to the current server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_address, server_port))

        # Forward the client socket to the server
        forward_data(self.client_socket, server_socket)

        # Close the server socket
        server_socket.close()

        # Close the client socket
        self.client_socket.close()


def round_robin_balancer():
    # Create a socket for the load balancer
    balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    balancer_socket.bind(('localhost', 9000))  # Port 9000 for load balancer
    balancer_socket.listen(10)

    print("Load balancer is running on port 9000...")

    while True:
        # Accept a client connection
        client_socket, client_address = balancer_socket.accept()
        print("Received connection from:", client_address)

        # Create a new thread to handle the client connection
        lb_thread = LoadBalancerThread(client_socket)
        lb_thread.start()

    # Close the load balancer socket
    balancer_socket.close()


def forward_data(source_socket, destination_socket):
    while True:
        data = source_socket.recv(1024)
        if not data:
            break
        destination_socket.sendall(data)

    source_socket.close()


if __name__ == '__main__':
    round_robin_balancer()
