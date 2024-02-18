import zmq
import numpy as np
from time import sleep
context = zmq.Context()

# Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:50165")

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

pygame.init()
utils.set_screen_dimensions()
# Set up the drawing window
screen = pygame.display.set_mode([utils.screen_width, utils.screen_height])
GRAY = (100, 100, 100)

font = pygame.font.Font("Fipps-Regular.otf",15)
fontBig = pygame.font.Font("Fipps-Regular.otf",19)
fontBigger = pygame.font.Font("Fipps-Regular.otf",23)
fontBiggest = pygame.font.Font("Fipps-Regular.otf",40)

p1 = player.WatchingPlayer()
fsm = player.ChatStateMachine() 

def get_center(surf):
    # Put the center of surf at the center of the display
    surf_center = (
        (utils.screen_width-surf.get_width())/2,
        (utils.screen_height-surf.get_height())/2
    )
    return surf_center

def facecam2pixel(x_loc):
    max_val = 450 # or 480 or 530 or 640
    max_pixel = utils.screen_width

    x = (max_pixel * (max_val - x_loc) / max_val) 
    return x
# Main loop
running = True
MOV_AVG_SIZE = 5
x_locs = np.ones(MOV_AVG_SIZE)
j = -1
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
    outputs = message.decode().split(";")
    # print(f"outputs:{outputs}")
    for i, face in enumerate(outputs):
        if face == "": continue
        # print(face)
        x_loc = face.split(":")[-1]
        # print(x_loc)
        # check if correct element kept from split
        if not (x_loc.replace(".","").replace("-","").isnumeric() and x_loc.count(".") <= 1 and x_loc.count("-") <= 1): continue

        x_loc = int(x_loc)
        # print(f"x_loc: {x_loc}")

        print("XLOC =", x_loc)
        if not np.any(x_locs - np.ones(MOV_AVG_SIZE)) and x_loc != -1:
            x_locs *= x_loc
        elif x_loc != -1:
            x_locs[j % MOV_AVG_SIZE] = x_loc

        avg_loc = np.mean(x_locs)
    x_pixel = facecam2pixel(avg_loc)

    # Update the player sprite based on user keypresses
    p1.update_eyes(x_pixel)
    p1.update_background()
    textbox_visible, text = p1.update_textbox(fsm=fsm, name="Jough")
    nf = int(x_loc != -1)
    print(f"nf:{nf}")

    fsm.update(nf=nf)
    print(fsm.get_state())
    # Fill the screen with black
    # screen.fill((200, 200, 200))
    screen.blit(p1.bg, p1.bg_rect)
    screen.blit(p1.surf, p1.rect)
    if textbox_visible:
        tb_text = fontBiggest.render(text,0,GRAY)
        screen.blit(p1.text_bubble, p1.tb_rect)
        screen.blit(tb_text, (utils.screen_width - 500, 100))

    pygame.display.flip()
    pygame.time.wait(100)

    

# Done! Time to quit.
pygame.quit()