# echo-server.py
from dQGenerativeModel import dQGenerativeModel
import time
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65431  # Port to listen on (non-privileged ports are > 1023)
SERVER_PORT = 65432 # Port used by the server
num_packets_received = 0

# Function for adding delay with more precision than time.sleep()
def sleep(duration):
    now = time.time()
    end = now + duration
    while now < end:
        now = time.time()

delaymodel = dQGenerativeModel()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.connect((HOST, SERVER_PORT)) # Connect to the server
        s.listen()
        conn, addr = s.accept() #Accept connection from the client
        while(num_packets_received < 100):
            with conn:
                while True:
                    data = conn.recv(1024) # Receive packet from client
                    if not data:
                        break
                    delay = delaymodel.get_delay(time.time())
                    sleep(delay) # Wait the required amount of time
                    s2.sendall(data) # Forward packet to server
                    num_packets_received += 1
                    data_from_server = s2.recv(1024) # Receive reply from server
                    conn.sendall(data_from_server) # Forward reply to client

class Delayer():
    def __init__(self) -> None:
        self.time_of_last_empty = 0
        self.queue = []
        self.delaymodel = dQGenerativeModel()
        
    def ingress(self, packet, timestamp):
        if self.queue == []:
            self.time_of_last_empty = timestamp
            self.queue.append((packet, timestamp + self.delaymodel.get_delay(timestamp)))
        else:
            time_since_last_empty = timestamp - self.time_of_last_empty
            self.queue.append((packet, time_since_last_empty + self.delaymodel.get_delay(timestamp)))

    def egress(self, conn, current_time):
        if self.queue != []:
            packet, scheduled_for = self.queue[0]
            if current_time >= scheduled_for:
                conn.sendall(packet)
                self.queue = self.queue[1:]