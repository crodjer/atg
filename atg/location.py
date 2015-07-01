'''
Get the timezone based on the provided location.
'''

import json
from urllib.parse import urlencode
from urllib.request import urlopen
from datetime import datetime


API_URL = "https://maps.googleapis.com/maps/api/{}/json?"

class LocationError(Exception):
    pass

def request(endpoint, **params):
    '''
    Make a request to a provide url, with params.
    '''

    response = urlopen(API_URL.format(endpoint) + urlencode(params))
    return json.loads(response.read().decode('utf-8'))

def geocode(location):
    '''
    Get the geocode information based on provided location.
    '''

    try:
        return request(
            "geocode",
            address=location,
            sensor="false"
        )['results'][0]['geometry']['location']
    except IndexError:
        raise LocationError('Could not find location: {}'.format(location))
    except KeyError:
        raise LocationError('Could not fetch coordinates')


def timezone(location, time=None):
    '''
    Get the timezone for a location.
    '''

    timestamp = (time or datetime.now()).timestamp()
    coordinates = geocode(location)

    return request("timezone", location="{lat},{lng}".format(**coordinates),
                   timestamp=timestamp)['timeZoneId']
