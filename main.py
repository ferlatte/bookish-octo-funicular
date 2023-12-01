#! /usr/bin/env python3

from icalendar import Calendar, Event # type: ignore
import requests

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
def cleanEventFromEvent(event: Event) -> Event:...

if __name__ == "__main__":
    print("Hello, world.")
