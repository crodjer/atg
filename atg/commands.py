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

COMMANDS = {}

def command(fn):
    '''
    Action decorator, just to keep a registry of actions.
    '''
    COMMANDS[fn.__name__] = fn
    return fn

@command
def timezone(args):
    '''
    Display their timezone.
    '''
    yield 'Their timezone is "{}"'.format(args.remote_tz)

@command
def now(args):
    '''
    Tell the current time there.
    '''
    yield 'Their time: {}'.format(U.now_str(args.remote_tz))

@command
def status(args):
    '''
    Get the probable status for people there.
    '''

    yield 'People there may be {}.'.format(
        U.status(args.remote_tz).status
    )

@command
def contact(args):
    '''
    Get convenient time slots to possibly contact the other person.
    '''

    reference = args.here_tz
    zipped_timeline = tuple(zip(U.timeline(args.here_tz, reference),
                                U.timeline(args.remote_tz, reference)))
    timeline_map = dict(zipped_timeline)

    def convenient(ht, rt):
        for a in args.dnd:
            if a.is_current(ht) and U.People.here in args.convenient_to:
                return False
            elif a.is_current(rt) and U.People.there in args.convenient_to:
                return False

        return True

    time_slots = U.grouped_time([
        ht
        for (ht, rt) in zipped_timeline
        if convenient(ht, rt)
    ])

    yield 'Convenient time slots:'
    for start, end, in time_slots:
        yield "\t{} to {} here, {} to {} there".format(
            start.strftime("%R"), end.strftime("%R"),
            timeline_map[start].strftime("%R"), timeline_map[end].strftime("%R")
        )


DEFAULT_COMMANDS = [timezone, now, status, contact]
@command
def default(args):
    '''
    The default action, executes a list of them.
    '''

    return (
        line
        for cmd in DEFAULT_COMMANDS
        for line in cmd(args)
    )
