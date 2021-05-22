# "send.py" can read queries from the "query.txt" file and send queries to the server.
# program can print current READ throughput to the screen.
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
path_query = "query.txt"
query_rate = 1000

len_key = 16

counter = 0


def counting():
    last_counter = 0
    while True:
        print(counter - last_counter), counter
        last_counter = counter
        time.sleep(1)


_thread.start_new_thread(counting, ())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f = open(path_query, "r")
interval = 1.0 / (query_rate + 1)
for line in f.readlines():
    line = line.split()
    op = line[0]
    key_header = int(line[1])
    key_body = line[2:]

    op_field = struct.pack("B", NC_READ_REQUEST)
    key_field = struct.pack(">I", key_header)
    for i in range(len(key_body)):
        key_field += struct.pack("B", int(key_body[i], 16))
    packet = op_field + key_field

    s.sendto(packet, (SERVER_IP, NC_PORT))
    counter = counter + 1
    time.sleep(interval)

f.close()