# atg: a small timezone utility
# Copyright (C) 2015 Rohan Jain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from atg import utils as U
from atg.activities import Activities

from datetime import datetime, timedelta
from pytz import utc, timezone

class TestUtils(unittest.TestCase):

    def test_now(self):
        naive_now = datetime.utcnow()
        now = U.now(utc)

        self.assertEqual(
            now.timetuple(),
            naive_now.replace(tzinfo=utc).timetuple()
        )


    def test_now_str(self):
        now = U.now(utc)
        self.assertEqual(now.strftime("%c"), U.now_str(utc), )

    def test_status(self):
        self.assertEqual(
            Activities.at(datetime.utcnow()),
            U.status(utc)
        )

    def test_timeline(self):
        delta = timedelta(minutes=30)
        _now = datetime.now()
        start = utc.localize(
            datetime(year=_now.year, month=_now.month, day=_now.day, hour=7)
        )

        self.assertEqual([
            (start + (delta * i))
            for i in range(48)
        ], U.timeline(utc, utc))

        london_tz = timezone('Europe/London')
        start = start.astimezone(london_tz)
        self.assertEqual([
            (start + (delta * i))
            for i in range(48)
        ], U.timeline(london_tz, utc))

    def test_grouped_time(self):
        delta = timedelta(minutes=30)
        start = utc.localize(
            datetime(year=2015, month=1, day=1, hour=7)
        )
        tl = [
            start, start + delta, start + delta * 2,
            start + delta * 5, start + delta * 7,
            start + delta * 9, start + delta * 10, start + delta * 11,
            start + delta * 12
        ]

        self.assertEqual([
            (start, start + delta * 2),
            (start + delta * 9, start + delta * 12)
        ], U.grouped_time(tl))
