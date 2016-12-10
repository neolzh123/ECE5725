#############################################################
# Function description: time_display.py
#   This function will display current time on piTFT screen
#   through pygame
#############################################################

import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import time, os

# define color white and black
BLACK = (0,0,0)
WHITE = (255,255,255)

# set display screen and mouse 
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 800, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Time Display')

# set font of text 
my_font = pygame.font.Font(None, 80)
my_font2 = pygame.font.Font(None, 30)

# define time display on screen
def time_display():
    # get current time and date
    cur_time = time.strftime('%I:%M:%S %p', time.localtime())
    cur_time2 = time.strftime('%a, %d %b %Y', time.localtime())
    # display time and date
    time_one = my_font.render(cur_time, True, WHITE)
    time_rect = time_one.get_rect(center = (400, 240))
    screen.blit(time_one, time_rect)
    time_two = my_font2.render(cur_time2, True, WHITE)
    time_rect2 = time_two.get_rect(center = (480, 300))
    screen.blit(time_two, time_rect2)
    # create quit button
    quit_button = my_font2.render('Quit', True, WHITE)
    quit_rect = quit_button.get_rect(center = (100, 440))
    screen.blit(quit_button, quit_rect)
    pygame.display.update()

startTime = time.time()
endTime = 0
gap = 5
# main loop
while endTime < startTime + 5:
    # Look for and process keyboard events to change modes.
    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif (event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            if quit_rect.collidepoint(pos):
                pygame.quit()
                
    # refresh screen display per second
    screen.fill(BLACK)
    time_display()
    endTime = time.time()
