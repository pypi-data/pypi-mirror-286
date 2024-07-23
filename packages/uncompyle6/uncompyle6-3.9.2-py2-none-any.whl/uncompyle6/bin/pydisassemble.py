#!/usr/bin/env python
#
#  Copyright (c) 2015-2016, 2018, 2020, 2022-2024
#  by Rocky Bernstein <rb@dustyfeet.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import getopt
import os
import sys

from uncompyle6.code_fns import disassemble_file
from uncompyle6.version import __version__

program, ext = os.path.splitext(os.path.basename(__file__))

__doc__ = """
Usage:
  %s [OPTIONS]... FILE
  %s [--help | -h | -V | --version]

Disassemble/Tokenize FILE with in the way that is done to
assist uncompyle6 in parsing the instruction stream. For example
instructions with variable-length arguments like CALL_FUNCTION and
BUILD_LIST have argument counts appended to the instruction name, and
COME_FROM pseudo instructions are inserted into the instruction stream.
Bit flag values encoded in an operand are expanding, EXTENDED_ARG
value are folded into the following instruction operand.

Like the parser, you may find this more high-level and or helpful.
However if you want a true disassembler see the Standard built-in
Python library module "dis", or pydisasm from the cross-version
Python bytecode package "xdis".

Examples:
  %s foo.pyc
  %s foo.py    # same thing as above but find the file
  %s foo.pyc bar.pyc  # disassemble foo.pyc and bar.pyc

See also `pydisasm' from the `xdis' package.

Options:
  -V | --version     show version and stop
  -h | --help        show this message

""" % (
    (program,) * 5
)

PATTERNS = ("*.pyc", "*.pyo")


def main():
    usage_short = (
        """usage: %s FILE...
Type -h for for full help."""
        % program
    )

    if len(sys.argv) == 1:
        sys.stderr.write("No file(s) given\n")
        sys.stderr.write(Usage_short)
        sys.exit(1)

    try:
        opts, files = getopt.getopt(
            sys.argv[1:], "hVU", ["help", "version", "uncompyle6"]
        )
    except getopt.GetoptError(e):
        sys.stderr.write("%s: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(-1)

    for opt, val in opts:
        if opt in ("-h", "--help"):
            print(__doc__)
            sys.exit(1)
        elif opt in ("-V", "--version"):
            print("%s %s" % (program, __version__))
            sys.exit(0)
        else:
            print(opt)
            sys.stderr.write(Usage_short)
            sys.exit(1)

    for file in files:
        if os.path.exists(files[0]):
            disassemble_file(file, sys.stdout)
        else:
            sys.stderr.write("Can't read %s - skipping\n" % files[0])
            pass
        pass
    return


if __name__ == "__main__":
    main()
