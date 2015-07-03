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
The command line interface for atg
'''

import argparse
from tzlocal import get_localzone

from .actions import ACTIONS
from .activities import Activities
from .location import timezone

P = argparse.ArgumentParser()
P.add_argument('--dnd', default=None, action='append',
               help='add a do not disturb activity (default: sleep)',
               choices=[a.name for a in Activities])
P.add_argument('-t', '--their', default=False, action='store_true',
               help='calculate everything from their reference frame')
P.add_argument('-m', '--my-location', default=None,
               help='specify your own location (default from system time)')
P.add_argument('-a', '--action', default='default', choices=ACTIONS.keys(),
               help='the action for atg to perform')

P.add_argument('remote', type=str,
               help='the remote location', nargs='+')

def client():
    '''
    The command line client.
    '''

    args = P.parse_args()
    args.dnd = [
        Activities[a]
        for a in args.dnd or []
    ]
    args.remote = ' '.join(args.remote)
    args.remote_tz = timezone(args.remote)
    if args.my_location:
        args.here, args.here_tz = args.my_location, timezone(args.my_location)
    else:
        args.here, args.here_tz = 'Here', get_localzone()

    if args.their:
        args.remote, args.here = args.here, args.remote
        args.remote_tz, args.here_tz = args.here_tz, args.remote_tz

    for line in ACTIONS[args.action](args):
        print(line)
