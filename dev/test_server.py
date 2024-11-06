import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
# server_socket.settimeout(0.05)
server_socket.listen(5)

conn, addr = server_socket.accept()
conn.settimeout(0.05)

while True:
    try:
        data = conn.recv(1024)
        if data:
            print(f'Received: {data} from {addr}')
            conn.send(data)
    except socket.timeout:
        continue
    except KeyboardInterrupt:
        conn.close()
        server_socket.close()
        break
    time.sleep(0.05)