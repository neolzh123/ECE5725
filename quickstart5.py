from __future__ import print_function
import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

import pygame
from pygame.locals import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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
pygame.display.set_caption('Calendar')

# set font of text 
my_font = pygame.font.Font(None, 40)
my_font2 = pygame.font.Font(None, 40)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
        
    i = 0
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        time_one = my_font.render(start, True, WHITE)
        time_rect = time_one.get_rect(center = (200, 50+30*i))
        screen.blit(time_one, time_rect)
        event = my_font.render(event['summary'], True, WHITE)
        event_rect = event.get_rect(center = (550, 50+30*i))
        screen.blit(event, event_rect)
        i = i + 1
        pygame.display.update()

# main loop
startTime = time.time()
endTime = 0
gap = 5
while endTime < startTime + 5:
    # Look for and process keyboard events to change modes.
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # On 'q' or keypad enter key, quit the program.
            if (( event.key == K_KP_ENTER ) or (event.key == K_q)):
                pygame.quit()
    # refresh screen display per second
    screen.fill(BLACK)
    main()
    endTime = time.time()
