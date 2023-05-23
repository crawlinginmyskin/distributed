import os
import threading
import paramiko
import tqdm
import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 2321
BUFFER_SIZE = 4096
SEPARATOR = "<s>"
lock = threading.Lock()


def handle_client(client_socket, address):
    global lock
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('<tajne ip>', username='<tajny user>', password='<tajne haslo>')

    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR, 1)
    filename = os.path.basename(filename)
    filesize = int(filesize.split(',')[0])
    print(f"[+] {address} is sending {filename} ({filesize} bytes)")

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with ssh_client.open_sftp() as sftp:
        with sftp.file(f"{filename}", "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                with lock:
                    f.write(bytes_read)
                    progress.update(len(bytes_read))

    client_socket.close()
    print(f"[+] {address} has finished sending {filename}")

    ssh_client.close()

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, address = s.accept()
    t = threading.Thread(target=handle_client, args=(client_socket, address))
    t.start()
