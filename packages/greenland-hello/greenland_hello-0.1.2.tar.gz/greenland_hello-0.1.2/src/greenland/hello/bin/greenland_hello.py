#
# greenland-hello - A minimal python project according to greenland conventions.
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

"""greenland-hello - Greenland demo project.

Usage:
  greenland-hello
  greenland-hello --version
  greenland-hello --product
  greenland-hello --program

Options:
  --version  Print version.
  --product  Print product.
  --program  Print program.
"""


from ..version import version, product, set_program
import sys
from docopt import docopt


def main(argv=sys.argv):

    program = set_program(argv[0])

    args = docopt(
        __doc__, argv=argv[1:], version=f"{program or product} {version}"
    )

    if args['--product']:
        print(product)
    elif args['--program']:
        print(program)
    else:
        print("Greenland says: Hi!")


if __name__ == '__main__':
    main()
