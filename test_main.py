import unittest
from icalendar import Calendar # type: ignore

import main

class TestMain(unittest.TestCase):
    def test_calendarFromICSFile(self) -> None:
        cal = main.calendarFromICSFile("test_cal1.ics")
        self.assertIsInstance(cal, Calendar)
        events = cal.walk("vevent")
        self.assertEqual(len(events), 1)

    def test_mergeEventsFromCalendars(self) -> None:
        cal1 = main.calendarFromICSFile("test_cal1.ics")
        cal2 = main.calendarFromICSFile("test_cal2.ics")
        cal = main.mergeEventsFromCalendars([cal1, cal2])
        events = cal.walk("vevent")
        self.assertEqual(len(events), 2)
