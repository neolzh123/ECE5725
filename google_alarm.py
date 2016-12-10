#!/usr/bin/env python
## Simple Google Calendar Alarm Clock
## Author: Xiyu

from __future__ import print_function
import httplib2
import os
import time
import datetime
import random
import logging  
from datetime import timedelta
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apscheduler.scheduler import Scheduler 

logging.basicConfig()


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
MP3_PATH = '/home/pi/ECE5725/Final/mp3/'


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

def format_utc_time(UTC_time):
    """ format utc time from "%Y-%m-%dT%H:%M:%S.%fZ" to "%Y-%m-%d %H:%M:%S"
    Input:
        utc time with format "%Y-%m-%dT%H:%M:%S.%fZ"
    Return:
        utc time with format "%Y-%m-%d %H:%M:%S"
    """
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    cur_utc_time = datetime.datetime.strptime(UTC_time, UTC_FORMAT)
    format_utc_time = cur_utc_time.strftime("%Y-%m-%d %H:%M")
    return format_utc_time

def event_utc_time(start_utc_time):
    """ convert current time to utc time
    """
    LOCAL_FORMAT = "%Y-%m-%d %H:%M:%S"
    time1 = start_utc_time[0:10]
    time2 = start_utc_time[11:19]
    time = time1 + " " + time2
    event_start_time = datetime.datetime.strptime(time, LOCAL_FORMAT)
    event_start_time += timedelta(hours = int(start_utc_time[21]))
    start_time = event_start_time.strftime("%Y-%m-%d %H:%M")
    return start_time

def event_query():
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
    cur_utc_time = format_utc_time(now)

    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            #print('----------------------------------------------')
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_start_time = event_utc_time(start)
            print(start," ", event['summary'])
            #print("event_start_time: {}, cur_utc_time: {}".format(event_start_time, cur_utc_time))
            #print(cur_utc_time)
            #print(event_start_time," ", event['summary'])
            if event_start_time == cur_utc_time:
                print("you have a schedule now")
                songfile = random.choice(os.listdir(MP3_PATH))
                print(songfile)
                #print "Now Playing:", songfile
                command = "mpg123"  + " " + MP3_PATH + songfile
                print(command)
                os.system(command)
            else:
                print("Wait for events")
            #print('----------------------------------------------')


def callable_func():
    os.system("clear")
    print("=============================")
    event_query()
    print("----------------------------")


sched = Scheduler(standalone=True)
sched.add_interval_job(callable_func,seconds=60)  #  define refresh rate. Set to every 10 seconds by default
sched.start()                                     #  runs the program indefinatly on an interval of x seconds

