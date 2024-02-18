import os
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

import cv2
import utils, client

grey_on = (69, 74, 68)
grey_off = (49, 51, 50)

frame_ranges = {
    "light_on": (0, 8),
    "transition_to_off": (9, 13),
    "light_off": (14, 21),
    "transition_to_on": (22, 39),
}

pygame.init()
utils.set_screen_dimensions()

screen = pygame.display.set_mode([utils.screen_width, utils.screen_height])

def get_center(surf):
    surf_center = (
        (utils.screen_width-surf.get_width())/2,
        (utils.screen_height-surf.get_height())/2
    )
    return surf_center

# Load the animation frames
animation_frames = []
for i in range(40):
    filename = f"frame_{i}_delay-0.05s.jpg"  # Replace with your actual filenames
    img = pygame.image.load(os.path.join('light-bear', 'anim', filename))  # Replace 'path_to_frames' with the path to your frames
    animation_frames.append(img)

# Variables to control the animation
frame_duration = 0.05  # Each frame lasts 0.05 seconds
current_frame = 0  # Start with the first frame
frame_time = 0  # Time since the last frame was displayed

# State machine variables
state = "light_off"
client.control_light(client.LIGHT_OFF)

# OpenCV face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    frame_time += dt  # Add the time since the last frame was displayed

    # Frame transitions
    if frame_time >= frame_duration:
        frame_time = 0  # Reset the frame timer
            
        # State transitions
        if state == "light_on" and current_frame == 8:
            # Face detection
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            face_detected = len(faces) > 0
            
            if face_detected:
                print("Face detected")
                current_frame = 0
            else:
                print("No face detected")
                state = "transition_to_off"
                client.control_light(client.LIGHT_OFF)
                current_frame += 1
        elif state == "transition_to_off" and current_frame == 13:
            state = "light_off"
            current_frame += 1            
        elif state == "light_off" and current_frame == 22:
            # Face detection
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            face_detected = len(faces) > 0
            
            if face_detected:
                print("Face detected")
                state = "transition_to_on"
                client.control_light(client.LIGHT_ON)
                current_frame += 1
            else:
                print("No face detected")
                current_frame = 14
        elif state == "transition_to_on" and current_frame == 39:
            state = "light_on"
            current_frame = 0
        else:
            current_frame += 1  # Go to the next frame 
        print(f"State: {state}, Frame: {current_frame}")
           
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    if current_frame >= 14 and current_frame <= 28:
        screen.fill(grey_off)
    else:
        screen.fill(grey_on)

    # Draw the current frame
    frame = animation_frames[current_frame]
    screen.blit(frame, get_center(frame))

    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
pygame.quit()