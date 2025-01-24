import pygame
import random
import time
import math
import maps

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
CYAN = (0,100,100)
RED = (255,0,0)
LIGHT_RED = (255,144,144)
LIGHT_BLUE = (135,206,235)
GREEN = (0,255,0)
DARK_GREEN = (1, 50, 32)
YELLOW = (255,255,0)
PURPLE = (160,32,240)

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


# Initializing pygame
pygame.init()
 
# Creating the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# Seting the title of the window
pygame.display.set_caption('Fboy and Wgirl')


def create_map(map):
        x = 0
        y = 0
        for i in map:
            for j in i:
                if j == 1:
                    pygame.draw.rect(screen, DARK_GREEN, [x,y, 10,10],0)

                # end if

                x += 10
            # next i
            x = 0
            y += 10
        # next j 