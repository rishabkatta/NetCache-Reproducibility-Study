#"receive.py" can receive replies from the server and the switch.
#program can print current READ throughput to the screen.
import socket
import struct
import time
import _thread

NC_READ_REQUEST     = 0
NC_READ_REPLY       = 1
NC_HOT_READ_REQUEST = 2
NC_WRITE_REQUEST    = 4
NC_WRITE_REPLY      = 5
NC_UPDATE_REQUEST   = 8
NC_UPDATE_REPLY     = 9


NC_PORT = 8888
CLIENT_IP = "10.0.0.1"
SERVER_IP = "10.0.0.2"
CONTROLLER_IP = "10.0.0.3"
path_reply = "reply.txt"

len_key = 16

counter = 0
def counting():
    last_counter = 0
    while True:
        print (counter - last_counter), counter
        last_counter = counter
        time.sleep(1)
_thread.start_new_thread(counting, ())


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((CLIENT_IP, NC_PORT))
while True:
    packet, addr = s.recvfrom(1024)
    counter = counter + 1
