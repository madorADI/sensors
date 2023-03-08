import time 
from cryptography.hazmat.backends import default_backend 
from cryptography.hazmat.primitives import serialization 
from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.asymmetric import padding

import socket
import json

def generate_full_message(message: bytes, id: str) -> bytes: 
    time_stamp = str(time.time()).ljust(19, "0")

    with open("private_key_{}.pem".format(id), "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    signature = private_key.sign(
        message + time_stamp.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )
    full_msg = time_stamp.encode() + id.encode() + signature + message
    
    return full_msg

def run_socket(data):
    UDP_IP = "10.200.3.12"
    server_id = "4"
    UDP_PORT = 8090
    MESSAGE = data.encode('utf8')
    crypted_message = generate_full_message(MESSAGE, server_id)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(crypted_message), (UDP_IP, UDP_PORT))
    print("UDP server up")

run_socket()