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
Definitions for actions supported by atg
'''

from atg import utils as U
from .activities import Activities


ACTIONS = {}

def action(fn):
    '''
    Action decorator, just to keep a registry of actions.
    '''
    ACTIONS[fn.__name__] = fn
    return fn

@action
def timezone(args):
    '''
    Display their timezone.
    '''
    yield 'Their timezone is "{}"'.format(args.remote_tz)

@action
def now(args):
    '''
    Tell the current time here and there.
    '''
    yield '{} in {}'.format(U.now_str(args.remote_tz), args.remote_tz)
    # yield '{} here'.format(U.now_str(args.here_tz))

@action
def activity(args):
    '''
    Get the probable activity people are doing there.
    '''

    yield 'People there may be {}.'.format(
        U.activity(args.remote_tz).status
    )

DEFAULT_ACTIONS = [now, activity]
@action
def default(args):
    '''
    The default action, executes a list of them.
    '''

    for act in DEFAULT_ACTIONS:
        for line in act(args):
            yield line
