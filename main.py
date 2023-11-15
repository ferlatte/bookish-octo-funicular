#! /usr/bin/env python3

from icalendar import Calendar, Event # type: ignore

def makeCalendar() -> Calendar:
    cal = Calendar()
    # PRODID and VERSION are required by RFC 5545
    cal.add("PRODID", "bookish-octo-funicular")
    cal.add("VERSION", "2.0")
    return cal

if __name__ == "__main__":
    print("Hello, world.")
    c = makeCalendar()
    print(c.to_ical())
