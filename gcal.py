#!/usr/bin/env python


import sys

from oauth2client import client
from googleapiclient import sample_tools
from datetime import datetime, timezone, timedelta


def get_events(hour_offset=12, long_term=False, long_term_offset=7, include_calendars=[]):
    """Returns a list of events

        Params:
         hour_offset - max hours in the future for events
         long_term - option to get events from more days (excluding the short-term defined by hour_offset)
         long_term_offset - number of days into the future (only used when long_term = True)
         include_calendars - calendars to be used, any calendars not in the list will be excluded

        Return:
         A list of the events within the given bounds with location information
    """
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        ['weatherApp.py', '--noauth_local_webserver'], 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')

    try:
        page_token = None
        start_time = datetime.now(timezone.utc).astimezone()        # current time
        time_offset = start_time + timedelta(hours = hour_offset)

        if long_term:
            start_time = time_offset
            time_offset = start_time + timedelta(days=long_term_offset)

        #Get all the calendar ids
        cal_ids = {}
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry['summary'] in include_calendars or not include_calendars:
                    cal_ids[calendar_list_entry['id']] = calendar_list_entry['summary']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        # cal_ids now has all ids for the users calendars
        # get all the events
        filtered_events = []
        for cid in cal_ids:
            while True:
                events = service.events().list(calendarId=cid, pageToken=page_token, timeMin=start_time.isoformat(), timeMax=time_offset.isoformat(), singleEvents=True).execute()

                for event in events['items']:
                    if 'location' in event:
                        filtered_events.append(event)

                page_token = events.get('nextPageToken')

                if not page_token:
                    break

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

    return filtered_events

if __name__ == '__main__':
    for event in get_events(include_calendars = ['Lab', 'Class', 'JHU', 'Personal']):
        print(event['summary']+' - '+event['start']['dateTime'])
        print(event.get('location'))
