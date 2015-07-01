import unittest

from atg.location import geocode, timezone

class TestLocation(unittest.TestCase):

    COORDINATE_FIXTURES = (
        ('San Francisco', {
            "lat": 37.7749295,
            "lng": -122.4194155
        }, 'America/Los_Angeles'),
        ('Jaipur', {
            "lat": 26.9124336,
            "lng": 75.7872709
        }, 'Asia/Calcutta')
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
