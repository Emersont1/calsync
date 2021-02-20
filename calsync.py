#!/usr/bin/env python
import requests
import caldav
import os

from icalendar import Calendar, Event

ups_urls = []
dav_url = ""
username = ""
password = ""

# Log into CalDAV
client = caldav.DAVClient(url=dav_url, username=username, password=password)
my_principal = client.principal()
calendar = my_principal.calendars()[0]

def add_events(dav_cal, upstream):
    # Get upstream ical
    r = requests.get(upstream)
    r.encoding = "utf-8"
    ical = r.text
    calendar = Calendar.from_ical(ical)
    for x in calendar.walk():
        if isinstance(x, Event):
            # Create individual Calendar for every event
            cal = Calendar()
            cal.add_component(x)

            # Search for event already in Calendar
            events = dav_cal.date_search(
                start=x.decoded('dtstart'), end=x.decoded('dtend'), expand=True)

            u = [e.vobject_instance.vevent.summary.value == x["summary"] for e in events]
            if not any(u):
                dav_cal.save_event(cal.to_ical())

for ups_url in ups_urls:
    add_events(calendar, ups_url)
