#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Color handling via ascii escape sequences
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

class color:
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m'
    CBLINK    = '\33[5m'
    CBLINK2   = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CCYAN   = '\33[36m'
    CWHITE  = '\33[37m'

    CBLACKBG  = '\33[40m'
    CREDBG    = '\33[41m'
    CGREENBG  = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG   = '\33[44m'
    CVIOLETBG = '\33[45m'
    CCYANBG   = '\33[46m'
    CWHITEBG  = '\33[47m'

    CGREY    = '\33[90m'
    CRED2    = '\33[91m'
    CGREEN2  = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2   = '\33[94m'
    CVIOLET2 = '\33[95m'
    CCYAN2   = '\33[96m'
    CWHITE2  = '\33[97m'

    CGREYBG    = '\33[100m'
    CREDBG2    = '\33[101m'
    CGREENBG2  = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2   = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CCYANBG2   = '\33[106m'
    CWHITEBG2  = '\33[107m'

# ------------------------------------------------------------------------------------------------------

# Python program to print
# colored text and background
class colors:
    off='\033[0m'
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'

    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        yellow='\033[33m'
        blue='\033[34m'
        magenta='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'

        boldgrey='\033[1;30m'
        boldred='\033[1;31m'
        boldgreen='\033[1;32m'
        boldyellow='\033[1;33m'
        boldblue='\033[1;34m'
        boldmagenta='\033[1;35m'
        boldcyan='\033[1;36m'
        boldwhite='\033[1;37m'

        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        lightyellow='\033[93m'
        lightblue='\033[94m'
        lightmagenta='\033[95m'
        lightcyan='\033[96m'

    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        yellow='\033[43m'
        blue='\033[44m'
        magenta='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

