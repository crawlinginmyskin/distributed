import socket
import tqdm
import os
import threading
import sys

SERVER_HOST = "0.0.0.0"
BUFFER_SIZE = 4096
SEPARATOR = "<s>"
lock = threading.Lock()


def handle_client(client_socket, address):
    global lock
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    print(f"[+] {address} is sending {filename} ({filesize} bytes)")

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(os.path.join("received", filename), "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            with lock:
                f.write(bytes_read)
                progress.update(len(bytes_read))
    client_socket.close()
    print(f"[+] {address} has finished sending {filename}")


def handle_file(client_socket, filename, filesize, address):
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(f'received/{filename}', "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    progress.close()
    print(f"[+] {address}: file {filename} received and saved.")


s = socket.socket()
SERVER_PORT = int(sys.argv[1])
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, address = s.accept()
    t = threading.Thread(target=handle_client, args=(client_socket, address))
    t.start()
