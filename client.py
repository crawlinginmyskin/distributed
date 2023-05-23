import socket
import tqdm
import os
import sys
from time import sleep
import paramiko

SEPARATOR = "<s>"
BUFFER_SIZE = 4096
host = '127.0.0.1'
port = 9000

if len(sys.argv) < 2:
    print("Usage: python client.py <file_path>")
    sys.exit(1)

filename = sys.argv[1]
if not os.path.exists(filename):
    print(f"{filename} does not exist")
    sys.exit(1)

filesize = os.path.getsize(filename)

s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
        sleep(0.001)
s.close()
