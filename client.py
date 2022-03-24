# echo-client.py
import time
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65431  # The port used by the delayer


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(100):
        s.sendall("Time is: {}".format(time.time()).encode('utf-8'))
        data = s.recv(1024)
        #print(f"Received {data!r}")
        data1, data2 = data.split(b'\t')
        time1 = float(str(data1).replace("b'Time is: ", "").replace("'", ""))
        time2 = float(str(data2).replace("b'Time is: ", "").replace("'", ""))
        print("Difference: {}s".format(time2-time1))