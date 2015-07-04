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

from pytz import timezone as l_timezone
from atg.location import geocode, timezone

class TestLocation(unittest.TestCase):

    COORDINATE_FIXTURES = (
        ('San Francisco', {
            "lat": 37.7749295,
            "lng": -122.4194155
        }, l_timezone('America/Los_Angeles')),
        ('Jaipur', {
            "lat": 26.9124336,
            "lng": 75.7872709
        }, l_timezone('Asia/Calcutta'))
    )

    def test_geocode(self):
        '''
        Check if we get correct lat/long values based on geocodes.
        '''

        for location, coordinates, _ in self.COORDINATE_FIXTURES:
            self.assertEqual(geocode(location), coordinates)

    def test_timezone(self):
        '''
        Check if correct timezones are loaded.
        '''

        for location, _, timezone_id in self.COORDINATE_FIXTURES:
            self.assertEqual(timezone(location), timezone_id)

    def test_direct_timezone(self):
        '''
        Check if directly passing timezones works.
        '''

        self.assertEqual(timezone('Asia/Calcutta'), l_timezone('Asia/Calcutta'))
