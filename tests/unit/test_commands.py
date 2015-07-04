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

from atg import utils as U
from atg import commands as C
from atg.activities import Activities

from pytz import timezone

class TestCommands(unittest.TestCase):

    def setUp(self):
        self.remote_tz = timezone('Europe/London')
        self.here_tz = timezone('Asia/Kolkata')
        self.dnd = [Activities.sleep.value]
        self.convenient_for = [U.People.here, U.People.there]

    def output(self, cmd):
        '''
        Get formatted string output for cmd.
        '''
        return '\n'.join(cmd(self))

    def in_command(self, cmd, string):
        '''
        Check if string exists in the command.
        '''

        self.assertIn(string, self.output(cmd))

    def test_timezone(self):
        self.in_command(C.timezone, self.remote_tz.zone)

    def test_now(self):
        self.in_command(C.now, U.now_str(self.remote_tz))

    def test_status(self):
        self.in_command(C.status, U.status(self.remote_tz).status)

    def test_schedule(self):
        self.in_command(C.schedule, "12:30 to 22:30")
        self.in_command(C.schedule, "08:00 to 18:00")

    def test_default(self):
        self.in_command(C.default, self.output(C.timezone))
        self.in_command(C.default, self.output(C.now))
        self.in_command(C.default, self.output(C.status))
        self.in_command(C.default, self.output(C.schedule))
