import socket
import time
from ground_core import SystemHeartbeat

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(0.05)
server_address = "robot.server" # "robot.server"
if client_socket.connect_ex((server_address, 12345)) != 0:
    client_socket.close()
    raise ConnectionRefusedError

while True:
    system_heartbeat = str(SystemHeartbeat((42.0, -71.0), "1"))
    print("sending")
    client_socket.send(system_heartbeat.encode())
    print("sent")
    starttime = time.time()
    while True:
        if time.time() - starttime > 3:
            break
        try:
            data = client_socket.recv(1024)
            if data:
                print(f'Received: {data}')
                break
        except socket.timeout:
            continue
        time.sleep(0.1)
