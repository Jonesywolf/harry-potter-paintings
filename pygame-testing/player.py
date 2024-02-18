import pygame, utils, os, time, random


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

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class WalkingPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super(WalkingPlayer, self).__init__()

        self.legs_wc = []
        self.legs_idle = []
        leg_wc_folder = ".\\legs-walk\\"
        for file in os.listdir(leg_wc_folder):
            # print(file)
            if file!="Thumbs.db":
                self.legs_wc.append(pygame.image.load(leg_wc_folder+file))
        
        leg_idle_folder = ".\\legs-idle\\"
        for file in os.listdir(leg_idle_folder):
            # print(file)
            if file!="Thumbs.db":
                self.legs_idle.append(pygame.image.load(leg_idle_folder+file))

        self.current_image = 0
        self.dt = 0.1
        self.max_dist = 0
        self.prev_time = time.time()
        # Use the first image to set the sprite's surface
        self.surf = self.legs_wc[self.current_image]
        self.rect = self.surf.get_rect() 
        self.rect.y = utils.screen_height - 400
        self.flipped = False

    # Move the sprite based on user keypresses
    def update(self, x_loc):
        prev_x = self.rect.x
        self.rect.x = x_loc
        
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        # if pressed_keys[K_LEFT]:
        #     self.rect.move_ip(-5, 0)
        # if pressed_keys[K_RIGHT]:        # self.rect.move_ip(5, 0)
        
        # Print the player's position
        print(x_loc, prev_x)
        print(f"FLIPPED:{self.flipped}")
        if abs(x_loc - prev_x) > 0.7 and (time.time() - self.prev_time) >= self.dt:
            self.prev_time = time.time()
            self.current_image = (self.current_image + 1) % len(self.legs_wc)
            self.surf = self.legs_wc[self.current_image]
            if x_loc - prev_x < 0:
                self.flipped = True
                self.surf = pygame.transform.flip(self.surf, flip_x=1, flip_y=0)
            else: self.flipped = False
        elif abs(x_loc - prev_x) < 0.2:
            self.surf = self.legs_idle[0]
            if self.flipped:
                self.surf = pygame.transform.flip(self.surf, flip_x=1, flip_y=0)

        print(self.rect.left, self.rect.right, self.rect.top, self.rect.bottom)
   
        # Keep player on the screen
        if self.rect.left < -100:
            self.rect.left = -100
        if self.rect.right > utils.screen_width:
            self.rect.right = utils.screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= utils.screen_height:
            self.rect.bottom = utils.screen_height

    def update_door(self):
        if self.rect.x  < -70:
            client.control_door()




class WatchingPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super(WatchingPlayer, self).__init__()
        self.eyes = []
        self.coffee = []
        self.text_bubbles = []
        eyes_folder = ".\\following-eyes\\"
        coffee_folder = ".\\coffee-imgs\\"
        text_bubble_folder = ".\\text-bubble\\"

        for file in os.listdir(coffee_folder):
            # print(file)
            if file!="Thumbs.db":
                self.coffee.append(pygame.image.load(coffee_folder+file))
                self.scale = (utils.screen_width /self.coffee[-1].get_width(), utils.screen_height / self.coffee[-1].get_height())
                self.coffee[-1] = pygame.transform.scale(self.coffee[-1], (utils.screen_width, utils.screen_height))

        for file in os.listdir(text_bubble_folder):
            # print(file)
            if file!="Thumbs.db":
                self.text_bubbles.append(pygame.image.load(text_bubble_folder+file))
                self.text_bubbles[-1] = pygame.transform.scale(self.text_bubbles[-1], (utils.screen_width, utils.screen_height))

        for file in os.listdir(eyes_folder):
            # print(file)
            if file!="Thumbs.db":
                self.eyes.append(pygame.image.load(eyes_folder+file))
                self.eyes[-1] = pygame.transform.scale(self.eyes[-1], (self.eyes[-1].get_width() * self.scale[0], self.eyes[-1].get_height() * self.scale[1]))

        self.neutral_x = utils.screen_width // 2
        self.current_image = 0

        # Use the first image to set the sprite's surface
        
        self.surf = self.eyes[0]
        self.bg = self.coffee[0]
        self.text_bubble = self.text_bubbles[0]

        self.rect = self.surf.get_rect() 
        self.rect.x = utils.screen_width // 2 - 57
        self.rect.y = utils.screen_height // 2 - 160

        self.bg_rect = self.bg.get_rect() 
        self.tb_rect = self.text_bubble.get_rect()
        self.flipped = False

        self.prev = 3
    # Move the sprite based on user keypresses
    def update_eyes(self, x_loc, debug=False):

        self.neutral_x
        
        if debug: 
            self.surf = self.eyes[0]
        elif (self.prev == 3 and x_loc > self.neutral_x + 100) or (self.prev != 3 and x_loc > self.neutral_x + 50):
            self.surf = self.eyes[1]
            self.prev = 1
        elif (self.prev == 3 and x_loc < self.neutral_x - 100) or (self.prev != 3 and x_loc < self.neutral_x - 50):
            self.surf = self.eyes[2]
            self.prev = 2
        elif x_loc > self.neutral_x - 50 and x_loc < self.neutral_x + 50 :
            self.surf = self.eyes[3]
            self.prev = 3

        # self.surf = pygame.transform.scale(self.surf, (self.surf.get_width() * self.scale[0], self.surf.get_height() * self.scale[1]))

    def update_background(self):
        if self.current_image == 0: 
            # TODO: do this in the main file not here
            rng_sample = random.randint(1,100)
            if rng_sample != 5: return
        # time.sleep(0.1)
        self.current_image = (self.current_image + 1) % len(self.coffee)
        self.bg = self.coffee[self.current_image]
        print("IMG SIZE:", self.bg.get_width(), self.bg.get_height())

    def update_textbox(self, fsm, name):
        state = fsm.get_state()
        if state == "textbox_visible":
            # self.
            return 1, f"Hello {name}"
        else: return 0, ""
        pass


class ChatStateMachine:
    def __init__(self):
        # Initial state
        self.state = 'ready'
        # Time since last transition
        self.prev_time = time.time()
        self.tt = 0

    def update(self, nf):   
        # Handle transitions from current state
        if self.state == 'ready':
            if nf > 0:
                self.state = 'textbox_visible'
                self.prev_time = time.time()
                self.tt = 0
        elif self.state == 'textbox_visible':
            self.tt = time.time() - self.prev_time
            if self.tt > 5:
                self.state = 'waiting'
        elif self.state == 'waiting':
            self.tt = time.time() - self.prev_time
            if nf == 0 and self.tt > 10:
                # Transition back to 'waiting' state, so no state change.
                self.tt = 0
                self.prev_time = time.time()
                self.state = 'ready'
            print(self.tt)

    def get_state(self):
        return self.state

class DoorStateMachine:
    def __init__(self):
        # Initial state
        self.state = 'closed'
        # Time since last transition
        self.prev_time = time.time()
        self.tt = 0
        self.set = 0
    def reset(self, x):
        if x >= 0:
            self.set = 0
    def update(self, x):   
        # Handle transitions from current state
        if self.state == 'closed':
            self.prev_time = time.time()
            self.tt = 0
            if x < -70 and self.set == 0:
                self.state = 'open'
                self.prev_time = time.time()
                self.tt = 0
                self.set = 1

        elif self.state == 'open':
            self.tt = time.time() - self.prev_time
            if self.tt > 5:
                self.state = 'closed'
            print(self.tt)

    def get_state(self):
        return self.state

# Example usage:
# fsm = StateMachine()
# for i in range(15):  # Simulate 15 time steps with nf=0
#     fsm.update(nf=0)
#     print(f"Time step {i}: State = {fsm.get_state()}")
# fsm.update(nf=1)  # Change nf to 1 to simulate a transition to 'ready'
# print(f"Transition: State = {fsm.get_state()}")
