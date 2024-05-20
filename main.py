#! /usr/bin/env python3

from icalendar import Calendar, Event # type: ignore
import requests
from flask import Flask, make_response, Response, abort
from markupsafe import escape
from dataclasses import dataclass

app = Flask(__name__)

@dataclass(frozen=True)
class User:
    """It's a user!"""
    id: str
    calendarFeeds: tuple[str, ...]

# TODO: hard coding the users to defer having to deal with persistent data.
Mark = User("mark", ("https://calendars.icloud.com/holidays/us_en-us.ics/",))
Test = User("test", ("URL3", "URL4"))
Users = {Mark.id: Mark,
         Test.id: Test
        }

@app.get("/hello")
def hello_world() -> str:
    return "<html><head></head><body><p>Hello, World!</p></body></html>"

@app.get("/schedule/<userId>")
def get_schedule_for_userid(userId) -> Response:
    try:
        u = Users[userId]
        calendars = []
        for feed in u.calendarFeeds:
            c = calendarFromURL(feed)
            calendars.append(c)
        schedule = mergeEventsFromCalendars(calendars)
        r = make_response(schedule.to_ical(), 200)
        r.headers["Content-Type"] = "text/calendar"
        return r
    except KeyError as err:
        abort(404)

def calendarFromURL(icsURL: str) -> Calendar:
    r = requests.get(icsURL)
    cal = Calendar.from_ical(r.text)
    return cal

def calendarFromICSFile(icsfile: str) -> Calendar:
    with open(icsfile) as f:
        icsData = f.read()
        cal = Calendar.from_ical(icsData)
        return cal

def makeCalendar() -> Calendar:
    cal = Calendar()
    # PRODID and VERSION are required by RFC 5545
    cal.add("PRODID", "bookish-octo-funicular")
    cal.add("VERSION", "2.0")
    return cal

# TODO: VTIMEZONE components need to be merged instead of copied, otherwise you have multiple TZID:America/Los_Angeles components
# from each calendar source.
def mergeEventsFromCalendars(calendars: list[Calendar]) -> Calendar:
    mergedCalendar = makeCalendar()
    for c in calendars:
        vevent: Event
        for vevent in c.walk("vevent"):
            mergedCalendar.add_component(vevent)
    return mergedCalendar

# VEVENT objects can carry a lot of information that, in theory, could be bad to leak.
# Instead of just doing a straight merge, we copy only the properties that are needed.
# DTSTAMP: Required
# UID : Required (but we should possibly generate our own)
# DTSTART: Start of event
# DTEND: End of event
# SUMMARY: This text appears at the title of the event
# TRANSP:TRANSPARENT consider hard coding this, since other people's schedules shouldn't be in the way of free/busy
# searches.
# RRULE: repeating event rules
# EXDATE: Excluded dates from the RRULE (ie, when you delete 1 event from a repeating event)
def cleanEventFromEvent(event: Event) -> Event:
    cleanEvent = Event()
    dtstamp = event.get('DTSTAMP')
    cleanEvent.add('DTSTAMP', dtstamp)
    uid = event.get('UID')
    cleanEvent.add('UID', uid)
    dtstart = event.get('DTSTART')
    cleanEvent.add('DTSTART', dtstart)
    dtend = event.get('DTEND')
    cleanEvent.add('DTEND', dtend)
    summary = event.get('SUMMARY')
    cleanEvent.add('SUMMARY', summary)
    cleanEvent.add('TRANSP', "TRANSPARENT")
    # TODO: these aren't working yet but we're moving forward and will fix them later when we need them
    # rrule = event.get('RRULE')
    # cleanEvent.add('RRULE', rrule)
    # exdate = event.get('EXDATE')
    # cleanEvent.add('EXDATE', exdate)
    return cleanEvent

if __name__ == "__main__":
    print("Hello, world.")
