#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI for exercising color handling
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import sys
import argcomplete, argparse

from .color_def import color, colors
from .color_show import shell_colors, color_fields

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}Color {color.CYELLOW2}attributes{color.CEND} for python scripts',
                    epilog='-.' * 40)

        subparsers = parser.add_subparsers(dest='cmd')

        parser_shellColors = subparsers.add_parser('shell.colors', help="display a color chart for current shell")
        parser_shellColors.add_argument('-e', '--extended', help="display extended chart", action="store_true")

        parser_colorFields = subparsers.add_parser('color.fields', help="display class color fields")

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.cmd == 'shell.colors':
            shell_colors(extended=args.extended)

        elif args.cmd == 'color.fields':
            color_fields()

    except Exception as e:
        # 2024-0706 - note - due to circular logic, exception_details is explicitly implemented below
        area = "Color Handling"
        print(f"\n{colors.fg.lightred}{type(e).__name__}{colors.fg.lightgrey} exception occurred in {colors.fg.cyan}{area}{colors.fg.lightgrey} processing!")
        exceptionArgs = e.args
        for arg in exceptionArgs:
            print(f"{colors.fg.lightblue}--> {colors.off}{arg}")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

