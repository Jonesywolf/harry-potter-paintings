import time
import zmq
import json
from datetime import datetime

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:50165")
import re

while True:
    #  Wait for next request from client
    message = socket.recv()

    message = str(message)
    print(datetime.now(),message)

    #  Send reply back to client
    socket.send(b"Data Recieved")