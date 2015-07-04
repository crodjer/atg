# atg: a little timezone utility
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
The command line interface for atg
'''

import argparse
import sys

from tzlocal import get_localzone

from .commands import COMMANDS
from .activities import Activities
from .location import timezone
from .utils import People

P = argparse.ArgumentParser()
P.add_argument('--dnd', default=None, action='append',
               help='the do not disturb activities (default: sleep)',
               choices=[a.name for a in Activities])
P.add_argument(
    '-c', '--convenient-for', default=None, action='append',
    choices=[p.name for p in People],
    help='which side\'s convenience should be considered (default: both)'
)
P.add_argument('-m', '--my-location', default=None,
               help='specify your own location (default from system time)')
P.add_argument('-x', '--command', default='default', choices=COMMANDS.keys(),
               help='the command for atg to execute')
P.add_argument('remote', type=str,
               help='the remote location', nargs='+')

def parse():
    '''
    Parse the command line arguments
    '''

    args = P.parse_args()
    if args.dnd is None:
        args.dnd = [Activities.sleep.value]
    else:
        args.dnd = [
            Activities[a].value
            for a in args.dnd
        ]

    if args.convenient_for is None:
        args.convenient_for = list(People)
    else:
        args.convenient_for = [People[g] for g in args.convenient_for]

    args.remote = ' '.join(args.remote)
    args.remote_tz = timezone(args.remote)
    if args.my_location:
        args.here, args.here_tz = args.my_location, timezone(args.my_location)
    else:
        args.here, args.here_tz = 'Here', get_localzone()

    return args

def client(out=sys.stdout):
    '''
    The command line client.
    '''
    args = parse()

    for line in COMMANDS[args.command](args):
        out.writelines(line + u'\n')
