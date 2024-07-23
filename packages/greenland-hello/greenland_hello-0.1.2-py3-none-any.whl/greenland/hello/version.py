#
# version.py -- Product / package and version information
# Copyright (C) 2024  M E Leypold
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
#

import subprocess
import os

version = None
version_tuple = None

def __editable_install__():
    return __file__[:-(len(__name__)+3)][-5:] == "/src/"

if not __editable_install__():
    try:
        from .__version__ import version, version_tuple
    except ModuleNotFoundError:
        pass

if version == None:
    from packaging.version import parse

    # TODO: Must CD to __file__
    
    r = subprocess.run(
        ["hatch", "version"], encoding = 'utf-8',
        cwd = os.path.dirname(__file__),
        capture_output = True, check = True
    )
    version = r.stdout.strip()
    __parsed__  = parse(version)
    version_tuple = (
        __parsed__.major, __parsed__.minor, __parsed__.micro, __parsed__.local
    )

product = "-".join(__name__.split('.')[:-1])
program = None

def set_program(name):
    global program
    program = os.path.basename(name)
    return program
