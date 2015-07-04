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

import unittest

import sys
from atg.activities import Activities
from atg.cli import parse, client
from atg.utils import People

from pytz import timezone
from tzlocal import get_localzone

class TestCli(unittest.TestCase):

    def setUp(self):
        self.remote_tz = 'Europe/London'
        self.my_tz = 'Asia/Kolkata'

    def parse_args(self, args=None):
        sys.argv = ['atg', self.remote_tz] + (args.split() if args else [])
        return parse()

    def test_basic_parse(self):
        args = self.parse_args()
        self.assertEqual(timezone(self.remote_tz), args.remote_tz)
        self.assertEqual(get_localzone(), args.here_tz)
        self.assertEqual({Activities.sleep.value}, set(args.dnd))
        self.assertEqual({People.there, People.here}, set(args.convenient_to))

    def test_parse_dnd(self):
        args = self.parse_args('--dnd work --dnd sleep')
        self.assertEqual({Activities.work.value, Activities.sleep.value},
                         set(args.dnd))

    def test_convenient_to(self):
        args = self.parse_args('-c here')
        self.assertEqual({People.here}, set(args.convenient_to))

        args = self.parse_args('--convenient-to there')
        self.assertEqual({People.there}, set(args.convenient_to))

        args = self.parse_args('-c there -c here')
        self.assertEqual({People.there, People.here}, set(args.convenient_to))

    def test_my_location(self):
        args = self.parse_args('-m ' + self.my_tz)
        self.assertEqual(timezone(self.my_tz), args.here_tz)
