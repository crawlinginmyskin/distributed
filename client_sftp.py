import socket
import os
import sys
import tqdm

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2321
BUFFER_SIZE = 4096
SEPARATOR = "<s>"


def send_file(file_path):
    file_name = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    print(file_name)
    print(filesize)
    s = socket.socket()
    print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
    s.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")

    s.send(f"{file_name}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file_path, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))

    s.close()
    print(f"[+] File {filename} sent successfully.")


if len(sys.argv) < 2:
    print("Usage: python client_sftp.py <file_path>")
    sys.exit(1)

filename = sys.argv[1]
if not os.path.exists(filename):
    print(f"{filename} does not exist")
    sys.exit(1)

send_file(filename)
