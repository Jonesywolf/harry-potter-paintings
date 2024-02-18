import pygame

screen_width = 0
screen_height = 0

def set_screen_dimensions():
    # Get the screen dimensions
    screen_info = pygame.display.Info()
    global screen_height
    global screen_width
    screen_height = screen_info.current_h
    screen_width = screen_info.current_w
    