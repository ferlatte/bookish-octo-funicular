#! /usr/bin/env python3

from icalendar import Calendar, Event # type: ignore
import requests
from flask import Flask, make_response
from markupsafe import escape

app = Flask(__name__)

@app.route("/hello")
def hello_world() -> str:
    return "<html><head></head><body><p>Hello, World!</p></body></html>"

@app.route("/schedule/<userid>")
def get_schedule_for_userid(userid) -> str:
    c = calendarFromICSFile("test_cal1.ics")
    r = make_response(c.to_ical(), 200)
    r.headers["Content-Type"] = "text/calendar"
    return r

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

def mergeEventsFromCalendars(calendars: list[Calendar]) -> Calendar:
    mergedCalendar = makeCalendar()
    for c in calendars:
        vevent: Event
        for vevent in c.walk("vevent"):
            mergedCalendar.add_component(vevent)
    return mergedCalendar



if __name__ == "__main__":
    print("Hello, world.")
