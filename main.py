#! /usr/bin/env python3

from icalendar import Calendar, Event, Timezone, vDDDTypes # type: ignore
import requests
from flask import Flask, make_response, Response, abort
from markupsafe import escape
from dataclasses import dataclass
from enum import StrEnum
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

class ICalendarComponent(StrEnum):
    EVENT = "VEVENT"
    TIMEZONE = "VTIMEZONE"

class ICalendarProperty(StrEnum):
    DTSTAMP = "DTSTAMP"
    UID = "UID"
    DTSTART = "DTSTART"
    DTEND = "DTEND"
    SUMMARY = "SUMMARY"
    TRANSP = "TRANSP"
    RRULE = "RRULE"
    EXDATE = "EXDATE"
    SEQUENCE = "SEQUENCE"
    RECURRENCE_ID = "RECURRENCE-ID"


@dataclass(frozen=True)
class User:
    """It's a user!"""
    id: str
    calendarFeeds: tuple[str, ...]

MARK_GCAL_URL=""
MARK_HOLIDAY_URL="https://calendars.icloud.com/holidays/us_en-us.ics/"

# TODO: hard coding the users to defer having to deal with persistent data.
Mark = User("mark", (MARK_HOLIDAY_URL, MARK_GCAL_URL))

Test = User("test", ("URL3", "URL4"))
Users = {Mark.id: Mark,
         Test.id: Test
        }

app = Flask(__name__)

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
        for vevent in c.walk(ICalendarComponent.EVENT):
            cleanEvent = cleanEventFromEvent(vevent)
            mergedCalendar.add_component(cleanEvent)
        vtimezone: Timezone
        for vtimezone in c.walk(ICalendarComponent.TIMEZONE):
            mergedCalendar.add_component(vtimezone)
    return mergedCalendar

# TODO: Figure out how to properly copy EXDATE
# VEVENT objects can carry a lot of information that, in theory, could be bad to leak.
# Instead of just doing a straight merge, we copy only the properties that are needed.
# DTSTAMP: Required
# UID : Required (but we should possibly generate our own)
# DTSTART: Start of event
# DTEND: End of event
# SUMMARY: This text appears at the title of the event
# TRANSP:TRANSPARENT hard code this, since other people's schedules shouldn't be in the way of free/busy
# searches.
# RRULE: repeating event rules
# EXDATE: Excluded dates from the RRULE (ie, when you delete 1 event from a repeating event)
def cleanEventFromEvent(event: Event) -> Event:
    cleanEvent = Event()
    cleanEvent.add(ICalendarProperty.TRANSP, "TRANSPARENT")
    standardDTSTAMP = standardizeDTSTAMP(event.get(ICalendarProperty.DTSTAMP))
    cleanEvent.add(ICalendarProperty.DTSTAMP, standardDTSTAMP)
    for p in (ICalendarProperty.DTEND,
              ICalendarProperty.DTSTART,
              ICalendarProperty.UID,
              ICalendarProperty.SUMMARY,
              ICalendarProperty.SEQUENCE,
              ICalendarProperty.RECURRENCE_ID):
        v = event.get(p)
        if (v):
            cleanEvent.add(p, v)
    return cleanEvent

def datetimeFromDate(d: date) -> datetime:
    return datetime.combine(d, time.min, ZoneInfo('UTC'))

# Many calendar systems seem to sometimes use a DATE for DTSTAMP instead of a
# DATE-TIME. Unfortunately, this violates RFC 5545 3.8.7.2. While it seems to work
# possibly all of the time, it breaks the validator so we fix it anyway.
def standardizeDTSTAMP(dtstamp: vDDDTypes) -> vDDDTypes:
    if (isinstance(dtstamp.dt, date)):
        timestamp = datetimeFromDate(dtstamp.dt)
        return vDDDTypes(timestamp)
    return dtstamp

if __name__ == "__main__":
    print("Hello, world.")
