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
