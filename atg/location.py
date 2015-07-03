# atg: find what time is it around the globe
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

'''
Get the timezone based on the provided location.
'''

import json
from pytz import timezone as l_timezone, UnknownTimeZoneError

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

    try:
        return l_timezone(location)
    except UnknownTimeZoneError:
        pass

    timestamp = (time or datetime.now()).timestamp()
    coordinates = geocode(location)

    return l_timezone(request(
        "timezone",
        location="{lat},{lng}".format(**coordinates),
        timestamp=timestamp
    )['timeZoneId'])
