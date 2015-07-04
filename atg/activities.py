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
Common major activities spanning a whole day
'''

from enum import Enum, unique

class Activity(object):
    '''
    Defines usual activities.
    '''

    _status = None

    @property
    def lower(self):
        return self.__class__.__name__.lower()

    @property
    def status(self):
        return self._status or self.lower + 'ing'

    def is_current(self, time):
        '''
        If this activity is the most probable activity in the given time.
        '''

        return time.hour in self.hours

class Work(Activity):
    hours = frozenset(range(10, 18))

class Sleep(Activity):
    hours = frozenset([23]).union(range(0, 8))

class Available(Activity):
    hours = frozenset(range(0, 24)) - Work.hours - Sleep.hours
    _status = 'available'


@unique
class Activities(Enum):

    work = Work()
    sleep = Sleep()
    available = Available()

    @classmethod
    def at(cls, time):
        '''
        The probable activity at given time.
        '''

        for activity in cls:
            if activity.value.is_current(time):
                return activity.value
