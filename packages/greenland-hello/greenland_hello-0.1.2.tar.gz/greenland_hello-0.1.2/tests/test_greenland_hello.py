#!/usr/bin/python
#
# greenland_test_hello -- Test greenland-hello
# Copyright (C) 2024  Markus E Leypold
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pytest import raises

from greenland.hello.bin.greenland_hello import main
from greenland.hello.version import version
import io
import sys

def test_main():

    try:
        saved_stdout = sys.stdout

        sys.stdout = main_stdout  = io.StringIO()
        main(["foo/bar/greenland-hello"])
        assert main_stdout.getvalue() == "Greenland says: Hi!\n"

        sys.stdout = main_stdout  = io.StringIO()
        main(["foo/bar/greenland-hello", "--product"])
        assert main_stdout.getvalue() == "greenland-hello\n"

        sys.stdout = main_stdout  = io.StringIO()
        main(["foo/bar/greenland-hello", "--program"])
        assert main_stdout.getvalue() == "greenland-hello\n"

        sys.stdout = main_stdout  = io.StringIO()

        with raises(SystemExit):
            main(["foo/bar/greenland-hello", "--version"])

        assert main_stdout.getvalue() == f"greenland-hello {version}\n"        
        
    finally:
        sys.stdout = saved_stdout
