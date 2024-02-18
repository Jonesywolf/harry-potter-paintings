import zmq
import numpy as np

from time import sleep
import os
import sys

# Simple pygame program
import player, utils

# Import and initialize the pygame library
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

sys.path.append('arduino-server')
import client

# Socket to talk to server
# def receive_data(port):
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.bind("tcp://127.0.0.1:5556")

# receive_data(5556)


pygame.init()
utils.set_screen_dimensions()
# Set up the drawing window
screen = pygame.display.set_mode([utils.screen_width, utils.screen_height])

p1 = player.WalkingPlayer()
fsm = player.DoorStateMachine() 

mansion_folder = "./mansion/"
mansion = []
for file in os.listdir(mansion_folder):
    # print(file)
    if file!="Thumbs.db":
        mansion.append(pygame.image.load(mansion_folder+file))

scale = (utils.screen_width / mansion[1].get_width(), utils.screen_height / mansion[1].get_height())
mansion[1] = pygame.transform.scale(mansion[1], (utils.screen_width, utils.screen_height))
mansion[0] = pygame.transform.scale(mansion[0], (mansion[0].get_width() * scale[0], mansion[0].get_height() * scale[1]))

mansion_rect = mansion[1].get_rect() 
mansion_edge_rect = mansion[0].get_rect() 



def get_center(surf):
    # Put the center of surf at the center of the display
    surf_center = (
        (utils.screen_width-surf.get_width())/2,
        (utils.screen_height-surf.get_height())/2
    )
    return surf_center

def facecam2pixel(x_loc):
    max_val = 400 # or 480 or 530 or 640
    max_pixel = utils.screen_width

    x = (max_pixel * (max_val - x_loc) / max_val) 
    return x
# Main loop
running = True
MOV_AVG_SIZE = 100
x_locs = np.ones(MOV_AVG_SIZE)
j = -1
avg_loc = p1.rect.x
opened = 0
while running:
    j += 1
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
            
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    socket.send(b"1Hello")
    sleep(0.01)
    #  Get the reply.
    message = socket.recv()
    print(message)
    if message is None: continue
    outputs = message.decode().split(";")

    for i, face in enumerate(outputs):
        if face == "": continue
        print(face)
        x_loc = face.split(":")[-1]
        # check if correct element kept from split
        if not (x_loc.replace(".","").isnumeric() and x_loc.count(".") <= 1): continue

        x_loc = int(x_loc)
        print("XLOC =", x_loc)
        if not np.any(x_locs - np.ones(MOV_AVG_SIZE)):
            x_locs *= x_loc
        else:
            x_locs[j % MOV_AVG_SIZE] = x_loc

        avg_loc = np.mean(x_locs)
    x_pixel = facecam2pixel(avg_loc)

    # Update the player sprite based on user keypresses
    p1.update(x_pixel)
    print(p1.rect.x)

    fsm.update(p1.rect.x)
    fsm.reset(p1.rect.x)
    
    if fsm.get_state() == "open" and not opened:
        client.control_door(client.DOOR_OPEN)
        # client.control_light(client.LIGHT_ON)
        opened = 1
    elif fsm.get_state() == "closed" and opened:
        client.control_door(client.DOOR_CLOSED)
        # client.control_light(client.LIGHT_OFF)
        opened = 0
    # Fill the screen with black
    # screen.fill((200, 200, 200))
    
    screen.blit(mansion[1], mansion_edge_rect)
    screen.blit(p1.surf, p1.rect)
    screen.blit(mansion[0], mansion_rect)

    pygame.display.flip()
    pygame.time.wait(10)

    

# Done! Time to quit.
pygame.quit()