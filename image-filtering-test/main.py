# Simple pygame program
import threading
import utils, capture_image
import math

# Import and initialize the pygame library
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
capture_image.load_images()
pygame.init()
utils.set_screen_dimensions()
# Set up the drawing window
screen = pygame.display.set_mode([utils.screen_width, utils.screen_height])

# Load the background image
background_image = pygame.image.load(r'image-filtering-test\background.jpg')

# Resize the background image
background_image = pygame.transform.scale(background_image, (utils.screen_width, utils.screen_height))

# Load another image
photographer_with_legs = pygame.image.load('image-filtering-test\photographer_legs.png')

photographer_position = (1000, 769)  # Change this to the position you want

# Load the animation images
animation_images = [pygame.image.load(fr'image-filtering-test\anim\photographer-{i}.png') for i in range(12)]

# Position for the animation
animation_position = (910, 400)  # Change this to the position you want

# Frame rate for the animation
frame_rate = 6

# Time to wait between animations (in milliseconds)
capture_interval = 10 * 1000  # Change this to the interval you want

# Time when the last animation was played
last_capture_time = 0

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# * Bobbing animation *
bob_animation_position = list(animation_position)
# Frequency of updates (in frames)
bob_update_frequency = 35  # Change this to the frequency you want

# Counter for the number of frames
bob_frame_counter = 0

# Create a thread that will run the capture_image function and store the result in result_list
capture_thread = threading.Thread(target=capture_image.capture_kawaii_image)

capturing = False

painting = None

painting_position = (610, 118)  # Change this to the position you want
painting_size = (275, 190)  # Change this to the size you want

def get_center(surf):
    # Put the center of surf at the center of the display
    surf_center = (
        (utils.screen_width-surf.get_width())/2,
        (utils.screen_height-surf.get_height())/2
    )
    return surf_center


def get_center(surf):
    # Put the center of surf at the center of the display
    surf_center = (
        (utils.screen_width-surf.get_width())/2,
        (utils.screen_height-surf.get_height())/2
    )
    return surf_center


# Main loop
running = True
while running:
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
    
    # Draw the background image on the screen
    screen.blit(background_image, (0, 0))
    
    # Draw the another image on the screen at the specified position
    screen.blit(photographer_with_legs, photographer_position)
    
    if painting:
        screen.blit(painting, painting_position)
    
    # Get the current time
    current_time = pygame.time.get_ticks()
    
    # If it's time to play the animation
    if current_time - last_capture_time >= capture_interval:
        # Start the thread
        capture_thread = threading.Thread(target=capture_image.capture_kawaii_image)
        capture_thread.start()
        capturing = True
        
        # Update the time when the last animation was played
        last_capture_time = current_time
        
        
    elif not capture_thread.is_alive() and capturing:
        # Play the animation
        for i in range(len(animation_images)):
            image = animation_images[i]
            if i == 6:
                # Fill the screen with white
                screen.fill((255, 255, 255))
                pygame.display.flip()
                capturing = False
                last_capture_time = current_time
                pygame.time.wait(250)  # wait
                painting = pygame.image.load('image-filtering-test\painting.jpg')
                painting = pygame.transform.scale(painting, painting_size)
            # Clear the screen by redrawing the background image
            screen.blit(background_image, (0, 0))
            # Draw the another image on the screen at the specified position
            screen.blit(photographer_with_legs, photographer_position)
            # Draw the current frame of the animation
            screen.blit(image, animation_position)
            if painting:
                screen.blit(painting, painting_position)
            pygame.display.flip()
            # Wait for the next frame
            clock.tick(frame_rate)
        
    else:
        # Only update the bobbing effect every nth frame
        if bob_frame_counter % bob_update_frequency == 0:
            bob_frame_counter = 0
            # Make the image bob up and down
            bob_animation_position[1] = 402 + math.sin(pygame.time.get_ticks() / 400) * 2  # Increase the speed and decrease the distance
        # Draw the first image of the animation
        screen.blit(animation_images[0], bob_animation_position)
        
    # Increment the frame counter
    bob_frame_counter += 1
    
    pygame.display.flip()
    

# Done! Time to quit.
pygame.quit()

capture_thread.join()