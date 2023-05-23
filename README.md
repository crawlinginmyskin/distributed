# distributed

## uzycie serwera
```
python3 server.py <port> 
```
domyslnie load balancer wysyla na porty 3234 i 3235, a sam load balancer operuje na porcie 9000

## uzycie klienta

```
python3 client.py <path/to/plik> 
```
klient wysyla plik na port 9000 gdzie znajduje sie load balancer

server_sftp i klient_sftp dzialaja na serwerze ssh 
