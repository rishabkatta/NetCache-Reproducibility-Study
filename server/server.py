"""
One Python program for the server. "server.py" can read key-value items from the "kv.txt" file,
and reply UPDATE queries from the controller and READ queries from the client.
In addition, this program can print current READ throughput to the screen.
"""

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

# NC_PORT = 8888
NC_PORT = 54999
CLIENT_IP = "10.0.0.1"
# SERVER_IP = "10.0.0.2"
SERVER_IP = "localhost"
CONTROLLER_IP = "10.0.0.3"
path_kv = "../generator/kv.txt"
path_log = "server_log.txt"

len_key = 16
len_val = 128

f = open(path_kv, "r")
lines = f.readlines()
f.close()

kv = {}
for i in range(2, 3002, 3):
    line = lines[i].split()
    key_header = line[0]
    key_body = line[1:]
    val = lines[i + 1].split()

    key_header = int(key_header)
    for i in range(len(key_body)):
        ## hexadecimal
        #print("For A, int is:", int('A', 16))
        key_body[i] = int(key_body[i], 16)
    for i in range(len(val)):
        val[i] = int(val[i], 16)

    key_field = ""
    key_field += struct.pack(">I", key_header)
    for i in range(len(key_body)):
        key_field += struct.pack("B", key_body[i])

    val_field = ""
    for i in range(len(val)):
        val_field += struct.pack("B", val[i])

    kv[key_header] = (key_field, val_field)
f.close()

counter = 0


def counting():
    last_counter = 0
    while True:
        print(counter - last_counter), counter
        last_counter = counter
        time.sleep(1)


_thread.start_new_thread(counting, ())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((SERVER_IP, NC_PORT))


while True:
    packet, addr = s.recvfrom(2048)
    op_field = packet[0]
    key_field = packet[1:]

    op = struct.unpack("B", op_field)[0]
    key_header = struct.unpack(">I", key_field[:4])[0]

    if op == NC_READ_REQUEST or op == NC_HOT_READ_REQUEST:
        op = NC_READ_REPLY
        op_field = struct.pack("B", op)
        key_field, val_field = kv[key_header]
        packet = op_field + key_field + val_field
        s.sendto(packet, (CLIENT_IP, NC_PORT))
        counter = counter + 1
    elif op == NC_UPDATE_REQUEST:
        op = NC_UPDATE_REPLY
        op_field = struct.pack("B", op)
        key_field, val_field = kv[key_header]
        packet = op_field + key_field + val_field
        s.sendto(packet, (CONTROLLER_IP, NC_PORT))
