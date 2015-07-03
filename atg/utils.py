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

from datetime import datetime

from .activities import Activities


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

def activity(tz):
    '''
    Given a TZ, guess the most probable activity.
    '''

    current_time = now(tz)

    for act in Activities:
        if act.value.is_current(current_time):
            return act.value
