#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Methods that show color codes in shell
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from .color_def import color, colors

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def shell_colors(extended: bool = False):
    if not extended:
        for style in range(8):
            for fg in range(30, 38):
                showColor = ''
                for bg in range(40, 48):
                    code = ';'.join([str(style), str(fg), str(bg)])
                    showColor = f'{showColor}\x1b[{code}m {code} \x1b[0m'
                print(showColor)
            print('\n')
    else:
        s1 = ''
        for bg in range(256):
            for fg in range(256):
                colorCode = ';'.join(['38', '5', str(fg), '48', '5', str(bg)])
                s1 += f'\x1b[{colorCode}m {colorCode:>22} \x1b[0m'
                if fg % 8 == 7:
                    print(s1)
                    s1 = ''

# ------------------------------------------------------------------------------------------------------

def color_fields():
    for idx, c in enumerate(dir(color)):
        derived_color = f'color.{c}'
        if 'C' in c:
            print(f"{eval(derived_color)}{c:<12}{color.CEND}", end='  ', flush=True)
            if idx % 8 == 7:
                print()

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

