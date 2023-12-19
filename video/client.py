import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import array
import numpy as np

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IPAddr, 8485))
connection = client_socket.makefile('wb')
print("Ip: ",IPAddr)


encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    _, frame = cv2.imencode('.jpg', frame, encode_param)
    client_socket.sendall(frame)
