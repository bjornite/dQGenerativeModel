# echo-server.py
import time
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
num_packets_received = 0
queue = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while(num_packets_received < 100):
        s.listen()
        conn, addr = s.accept()
        with conn:
            #print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                added_timestamp = "\tTime is: {}".format(time.time()).encode('utf-8')
                conn.sendall(data + added_timestamp)
                num_packets_received += 1
