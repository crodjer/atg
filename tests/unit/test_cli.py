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

# pylint: disable=F0401

import unittest

import sys
from atg.activities import Activities
from atg.cli import parse, client
from atg.utils import People

from io import StringIO
from pytz import timezone
from tzlocal import get_localzone

class TestCli(unittest.TestCase):

    def setUp(self):
        self.remote_tz = 'Europe/London'
        self.my_tz = 'Asia/Kolkata'

    def setup_args(self, args=None):
        sys.argv = ['atg', self.remote_tz] + (args.split() if args else [])

    def parse_args(self, args=None):
        self.setup_args(args)
        return parse()

    def test_basic_parse(self):
        args = self.parse_args()
        self.assertEqual(timezone(self.remote_tz), args.remote_tz)
        self.assertEqual(get_localzone(), args.here_tz)
        self.assertEqual({Activities.sleep.value}, set(args.dnd))
        self.assertEqual({People.there, People.here}, set(args.convenient_for))

    def test_my_tz(self):
        args = self.parse_args('-m ' + self.my_tz)
        self.assertEqual(timezone(self.my_tz), args.here_tz)

    def test_parse_dnd(self):
        args = self.parse_args('--dnd work --dnd sleep')
        self.assertEqual({Activities.work.value, Activities.sleep.value},
                         set(args.dnd))

    def test_convenient_for(self):
        args = self.parse_args('-c here')
        self.assertEqual({People.here}, set(args.convenient_for))

        args = self.parse_args('--convenient-for there')
        self.assertEqual({People.there}, set(args.convenient_for))

        args = self.parse_args('-c there -c here')
        self.assertEqual({People.there, People.here}, set(args.convenient_for))

    def test_client(self):
        out = StringIO()
        self.setup_args('-x timezone')
        client(out=out)
        self.assertIn(self.remote_tz, out.getvalue())
