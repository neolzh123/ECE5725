#############################################################
# Function description: time_display.py
#   This function will display current time on piTFT screen
#   through pygame
#############################################################

import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import time, os

class TimeDisp:
    def __init__(self):
        # define color white and black
        BLACK = (0,0,0)
        WHITE = (255,255,255)

        # set display screen and mouse 
        os.putenv('SDL_FBDEV', '/dev/fb1')
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.putenv('SDL_MOUSEDRV', 'TSLIB')
        os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

        pygame.init()
        pygame.mouse.set_visible(True)
        size = width, height = 800, 480
        self.screen = pygame.display.set_mode(size)

        # set font of text 
        my_font = pygame.font.Font(None, 80)
        my_font2 = pygame.font.Font(None, 30)

    # define time display on screen
    def time_display(self):
        # get current time and date
        cur_time = time.strftime('%I:%M:%S %p', time.localtime())
        cur_time2 = time.strftime('%a, %d %b %Y', time.localtime())
        # display time and date
        time_one = my_font.render(cur_time, True, WHITE)
        time_rect = time_one.get_rect(center = (400, 240))
        self.screen.blit(time_one, time_rect)
        time_two = my_font2.render(cur_time2, True, WHITE)
        time_rect2 = time_two.get_rect(center = (480, 300))
        self.screen.blit(time_two, time_rect2)
        pygame.display.update()

    def time_update(self):  
        # main loop
        while True:
            # Look for and process keyboard events to change modes.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # On 'q' or keypad enter key, quit the program.
                    if (( event.key == K_KP_ENTER ) or (event.key == K_q)):
                        pygame.quit()
            # refresh screen display per second
            self.screen.fill(BLACK)
            time_display()
