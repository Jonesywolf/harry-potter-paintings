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

p1 = player.Player()


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
            
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    p1.update(pressed_keys)
    
    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    screen.blit(p1.surf, p1.rect)

    pygame.display.flip()
    

# Done! Time to quit.
pygame.quit()