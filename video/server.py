import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib


hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname) 
HOST=IPAddr
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind completo')
s.listen(10)
print('Socket escutando...')

conn,addr=s.accept()


while True:
    data = conn.recv(409600)
    frame = cv2.imdecode(np.frombuffer(data, dtype = 'uint8') , cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    key = cv2.waitKey(1) & 0xFF


