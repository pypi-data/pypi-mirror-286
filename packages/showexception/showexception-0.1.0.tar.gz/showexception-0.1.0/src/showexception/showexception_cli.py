#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI for exception display handling
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import sys

from quickcolor.color_def import color

from .showexception import exception_details

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli():
    runRaw = False
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CRED2}Exception Content Display{color.CEND} for python scripts',
                    epilog='-.' * 40)

        parser.add_argument('-r', '--raw', action='store_true', help='show raw exception details')

        subparsers = parser.add_subparsers(dest='cmd')

        parser_testZeroDiv = subparsers.add_parser('test.zero.div', help='display exception info for a divide by zero exception')

        parser_testNameErr = subparsers.add_parser('test.name.err', help='display exception info for a name error exception')

        parser_testTypeErr = subparsers.add_parser('test.type.err', help='display exception info for a type error exception')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        runRaw = args.raw

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.cmd == 'test.zero.div':
            testVar = 1/0

        elif args.cmd == 'test.name.err':
            testVar = y + 5

        elif args.cmd == 'test.type.err':
            x = 'b'
            testVar = x + 5

    except Exception as e:
        exception_details(e, 'Exception Handling', raw=runRaw)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

