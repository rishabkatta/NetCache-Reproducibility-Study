import thread
import socket
import struct
import time

NC_READ_REQUEST = 0
NC_READ_REPLY = 1
NC_HOT_READ_REQUEST = 2
NC_WRITE_REQUEST = 4
NC_WRITE_REPLY = 5
NC_UPDATE_REQUEST = 8
NC_UPDATE_REPLY = 9


NC_PORT = 8888
CLIENT_IP = "10.0.0.1"
SERVER_IP = "10.0.0.2"
CONTROLLER_IP = "10.0.0.3"
path_hot = "hot.txt"
path_log = "controller_log.txt"

len_key = 16
len_val = 128

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((CONTROLLER_IP, NC_PORT))

op = NC_UPDATE_REQUEST
op_field = struct.pack("B", op)
f = open(path_hot, "r")
for line in f.readlines():
    line = line.split()
    key_header = line[0]
    key_body = line[1:]
    
    key_header = int(key_header)
    for i in range(len(key_body)):
        key_body[i] = int(key_body[i], 16)
    
    key_field = ""
    key_field += struct.pack(">I", key_header)
    for i in range(len(key_body)):
        key_field += struct.pack("B", key_body[i])
    
    packet = op_field + key_field
    s.sendto(packet, (SERVER_IP, NC_PORT))
    time.sleep(0.001)
f.close()

while True:
    packet, addr = s.recvfrom(2048)
    op_field = packet[0]
    key_field = packet[1:len_key + 1]
    load_field = packet[len_key + 1:]
    
    op = struct.unpack("B", op_field)[0]
    if (op != NC_HOT_READ_REQUEST):
        continue
    
    key_header = struct.unpack(">I", key_field[:4])[0]
    load = struct.unpack(">IIII", load_field)
    
    counter = counter + 1
    print("\tHot Item:", key_header, load)
