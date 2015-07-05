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
Basic utils used across atg
'''

from datetime import datetime, timedelta
from itertools import groupby
from enum import Enum, unique

from .activities import Activities

HALF_HOUR = timedelta(minutes=30)

@unique
class People(Enum):
    '''
    Enum for the two locations.
    '''
    here = 0
    there = 1

def now(tz):
    '''
    Get the current time for tz.
    '''
    return datetime.now(tz)

def now_str(tz):
    '''
    Get the current time as string, formatted based on locale.
    '''
    return now(tz).strftime("%c")

def status(tz):
    '''
    Given a TZ, guess the most probable activity.
    '''
    return Activities.at(now(tz))

DAY_HOURS = tuple(range(0, 24))

def timeline(tz, reference, start=7):
    '''
    Get the timeline for a timezone.
    '''

    _now = datetime.now(tz)
    start = reference.localize(
        datetime(year=_now.year, month=_now.month, day=_now.day, hour=start)
    ).astimezone(tz)

    return [
        (start + (HALF_HOUR * i))
        for i in range(48)
    ]

def grouped_time(tl):
    '''
    Provide the grouped times based on a timeline with half hour offsets.
    '''

    # Python 3 doesn't have reduces, hence a for loop
    acc = []
    for time in tl:
        if acc == []:
            acc = [(time, time + HALF_HOUR)]
            continue

        prev_s, prev_e = acc[-1]
        if prev_e == time:
            acc[-1] = (prev_s, time + HALF_HOUR)
        else:
            acc.append((time, time + HALF_HOUR))

    return acc
