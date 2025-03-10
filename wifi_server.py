from picarx import Picarx
import time
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue
import subprocess
import socket

#PiCar variables
straight = -2

end_y = 25 #in 15 cm
end_x = 34

current_y = 20 #start in bottom middle
current_x = 40

POWER = 50

map_w = 40 #40x40 grid, i.e. 6x6 meters
map_h = 60

SafeDistance = 40   # > 40 safe
DangerDistance = 25 # > 20 && < 40 turn around, 
                    # < 20 backward
pan_max = 45
diff_threshold = 14
pan_diff = 5
tilt_angle = 11



HOST = "100.72.143.10" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)



		

def forward(px):    #15cm
	print("in forward function")
	px.set_dir_servo_angle(straight)
	px.forward(POWER)
	time.sleep(1.5)
	px.forward(0) 
	time.sleep(.25)
	
def backward(px):    
	px.set_dir_servo_angle(straight)
	px.backward(POWER)
	time.sleep(.75)
	px.forward(0) 
	time.sleep(.25)
		
def right_turn(px, client):
	for i in range(3):
		px.set_dir_servo_angle(straight)
		time.sleep(.25)
		px.forward(POWER)
		time.sleep(1)
		px.forward(0)
		px.set_dir_servo_angle(straight-35)
		client.sendall(("left").encode())
		time.sleep(.25)
		px.backward(POWER)
		time.sleep(.8)
		px.forward(0) 
		client.sendall(("center").encode())
		px.set_dir_servo_angle(straight)
		time.sleep(.25)
	return 
		
def left_turn(px, client):
	for i in range(3):
		px.set_dir_servo_angle(straight)
		time.sleep(.25)
		px.forward(POWER)
		time.sleep(1)
		px.forward(0)
		px.set_dir_servo_angle(straight+35)
		client.sendall(("right").encode())
		time.sleep(.25)
		px.backward(POWER)
		time.sleep(.8)
		px.forward(0) 
		client.sendall(("center").encode())
		px.set_dir_servo_angle(straight)
		time.sleep(.25)
	return





with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        px = Picarx()
        px.set_cam_tilt_angle(tilt_angle) 
        px.set_dir_servo_angle(straight)
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                client.sendall(("moving").encode())
                print(data)    
                if data== b'forward\r\n':
                    print("moving forward")
                    forward(px)
                if data==b'backward\r\n':
                    backward(px)
                if data==b'left\r\n':
                    left_turn(px,client)
                if data==b'right\r\n':
                    right_turn(px,client)
                print("reading")
                distance = round(px.ultrasonic.read(), 2) 
                distance = str(distance).encode()
                print(distance)
                client.sendall(distance) # Echo back to client
                client.sendall(("done").encode())
                print("data sent")
    except: 
        print("Closing socket")
        client.close()
        s.close()    






