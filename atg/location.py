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

'''
Get the timezone based on the provided location.
'''

# pylint: disable=E0611,F0401

import json
from pytz import timezone as l_timezone, UnknownTimeZoneError

try:
    from urllib.parse import urlencode # pragma: no cover
    from urllib.request import urlopen # pragma: no cover
except ImportError:                    # pragma: no cover
    from urllib2 import urlopen        # pragma: no cover
    from urllib import urlencode       # pragma: no cover

from time import time


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
        response = request(
            "geocode",
            address=location,
            sensor="false"
        )

        return response['results'][0]['geometry']['location']
    except IndexError:
        raise LocationError(
            'Could not find location: {} in {}'.format(
                location, json.dumps(response, indent=2)
            )
        )
    except KeyError:                                       # pragma: no cover
        raise LocationError('Could not fetch coordinates') # pragma: no cover

def timezone(location):
    '''
    Get the timezone for a location.
    '''

    try:
        return l_timezone(location)
    except UnknownTimeZoneError:
        pass

    timestamp = time()
    coordinates = geocode(location)

    return l_timezone(request(
        "timezone",
        location="{lat},{lng}".format(**coordinates),
        timestamp=timestamp
    )['timeZoneId'])
