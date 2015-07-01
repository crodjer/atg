'''
Possible activities.
'''

from enum import Enum, unique

class Activity(object):
    '''
    Defines usual activities.
    '''

    def is_current(self, time):
        '''
        If this activity is the most probable activity in the given time.
        '''

        return time.hour in self.hours

    def __repr__(self):
        return self.__class__.__name__

class Work(Activity):
    hours = frozenset(range(10, 18))

class Sleep(Activity):
    hours = frozenset([23]).union(range(0, 8))

class Free(Activity):
    hours = frozenset(range(0, 24)) - Work.hours - Sleep.hours

@unique
class Activities(Enum):

    work = Work()
    sleep = Sleep()
    free = Free()
