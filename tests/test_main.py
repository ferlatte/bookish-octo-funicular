import unittest
from icalendar import Calendar, Event
from zoneinfo import ZoneInfo
from datetime import date, datetime, timedelta
from uuid import uuid4

import main

def makeTestEvent() -> Event:
    e = Event()
    now = datetime.now(ZoneInfo("UTC"))
    one_hour = timedelta(hours=1)
    e.add('DTSTART', now)
    e.add('SUMMARY', "Test Event")
    e.add('UID', uuid4().hex)
    e.add('DTEND', now + one_hour)
    e.add('DTSTAMP', now)
    e.add('X-BAD', "SUPER SECRET DATA OH NO")
    return e

def makeTestEventWithBrokenDTSTAMP() -> Event:
    e = Event()
    now = datetime.now(ZoneInfo("UTC"))
    one_hour = timedelta(hours=1)
    # DTSTAMP MUST be a datetime, but some systems (like Apple's holiday caledar) use DATE by mistake.
    dtstamp_date = date(1976, 4, 1)
    e.add('DTSTART', now)
    e.add('SUMMARY', "Test Event With Broken DTSTAMP")
    e.add('UID', uuid4().hex)
    e.add('DTEND', now + one_hour)
    e.add('DTSTAMP', dtstamp_date)
    return e

class TestMain(unittest.TestCase):

    def test_calendarFromURL(self) -> None:
        url = "https://calendars.icloud.com/holidays/us_en-us.ics/"
        cal = main.calendarFromURL(url)
        events = cal.walk("vevent")
        self.assertGreaterEqual(len(events), 1)

    def test_calendarFromICSFile(self) -> None:
        cal = main.calendarFromICSFile("tests/test_cal1.ics")
        self.assertIsInstance(cal, Calendar)
        events = cal.walk("vevent")
        self.assertEqual(len(events), 1)

    def test_mergeEventsFromCalendars(self) -> None:
        cal1 = main.calendarFromICSFile("tests/test_cal1.ics")
        cal2 = main.calendarFromICSFile("tests/test_cal2.ics")
        cal = main.mergeEventsFromCalendars([cal1, cal2])
        events = cal.walk("vevent")
        self.assertEqual(len(events), 2)

    def test_cleanEventFromEvent(self) -> None:
        e = makeTestEvent()
        self.assertEqual(e.get('X-BAD'), 'SUPER SECRET DATA OH NO')
        cleanEvent = main.cleanEventFromEvent(e)
        self.assertIsNone(cleanEvent.get('X-BAD'))

    def test_standardizeDTSTAMP(self) -> None:
        e = makeTestEventWithBrokenDTSTAMP()
        broken_dtstamp = e.get(main.ICalendarProperty.DTSTAMP)
        self.assertIsInstance(broken_dtstamp.dt, date)
        fixed_dtstamp = main.standardizeDTSTAMP(broken_dtstamp)
        self.assertIsInstance(fixed_dtstamp.dt, datetime)

    def test_user(self) -> None:
        u = main.User("test", ("https://example.com/calendar1.ics", "https://example.com/calendar2.ics"))
        self.assertEqual(len(u.calendarFeeds), 2)




