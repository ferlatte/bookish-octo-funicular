#! /usr/bin/env python3

from icalendar import Calendar, Event # type: ignore

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

def mergeEventsFromCalendars(calendars: list[Calendar]) -> Calendar:
    mergedCalendar = makeCalendar()
    for c in calendars:
        vevent: Event
        for vevent in c.walk("vevent"):
            mergedCalendar.add_component(vevent)
    return mergedCalendar



if __name__ == "__main__":
    print("Hello, world.")
