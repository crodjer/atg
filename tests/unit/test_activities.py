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

from atg.activities import Activities
from datetime import time

A = Activities

class ActivitiesTest(unittest.TestCase):

    EXPECTED_ACTIVITIES = (
        (0, A.sleep),
        (1, A.sleep),
        (2, A.sleep),
        (3, A.sleep),
        (4, A.sleep),
        (5, A.sleep),
        (6, A.sleep),
        (7, A.sleep),
        (8, A.available),
        (9, A.available),
        (10, A.work),
        (11, A.work),
        (12, A.work),
        (13, A.work),
        (14, A.work),
        (15, A.work),
        (16, A.work),
        (17, A.work),
        (18, A.available),
        (19, A.available),
        (20, A.available),
        (21, A.available),
        (22, A.available),
        (23, A.sleep)
    )

    def test_is_current(self):
        '''
        Current hour check is working
        '''

        activities = set(Activities)

        for hour, activity in self.EXPECTED_ACTIVITIES:
            t = time(hour=hour)
            self.assertTrue(
                activity.value.is_current(t),
                '{} should be {} time'.format(t, str(activity.name))
            )

            for o_activity in activities - {activity}:
                self.assertFalse(
                    o_activity.value.is_current(t),
                    '{} should not be {} time'.format(t, str(o_activity.name))
                )


    def test_get_activity_at_time(self):
        '''
        Check if correct activity is guessed given a time.
        '''

        self.assertEqual(Activities.at(time(hour=1)), A.sleep.value)
        self.assertEqual(Activities.at(time(hour=10)), A.work.value)
        self.assertEqual(Activities.at(time(hour=20)), A.available.value)


    def test_status(self):
        '''
        Activities have correct statuses
        '''

        self.assertEqual(Activities.work.value.status, 'working')
        self.assertEqual(Activities.sleep.value.status, 'sleeping')
        self.assertEqual(Activities.available.value.status, 'available')
