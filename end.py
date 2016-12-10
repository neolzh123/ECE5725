#############################################################
# Function description: time_display.py
#   This function will display current time on piTFT screen
#   through pygame
#############################################################

import pygame
from pygame.locals import *
import time, os

# define color white and black
BLACK = (0,0,0)
WHITE = (255,255,255)

# set display screen and mouse 
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 800, 480
screen = pygame.display.set_mode(size)

# set font of text 
my_font = pygame.font.Font(None, 80)

# define time display on screen
def ending():
    screen.fill(WHITE)
    smile = pygame.image.load('happy.png')
    smile = pygame.transform.scale(smile, (250,250))
    smile_rect = smile.get_rect(center=(width/4,height/2))
    text = 'Enjoy your day!'
    greeting = my_font.render(text, True, BLACK)
    greeting_rect = greeting.get_rect(center = (width*0.7, height/2))
    screen.blit(greeting, greeting_rect)
    screen.blit(smile, smile_rect)
    pygame.display.update()
   
# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # refresh screen display per second
    ending()

        

