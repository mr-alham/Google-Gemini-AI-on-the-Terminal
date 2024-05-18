#!/bin/env python3
"""ansi color codes"""


def ansi(color_list: list[str]) -> str:
    """Returns a string of ansi color codes"""

    tags = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "inverse": "\033[7m",
        "hide": "\033[8m",
        "strikethrough": "\033[9m",
        "black": "\033[30m",  # colors
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_black": "\033[90m",  # bright colors
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
        "black_bg": "\033[40m",  # background colors
        "red_bg": "\033[41m",
        "green_bg": "\033[42m",
        "yellow_bg": "\033[43m",
        "blue_bg": "\033[44m",
        "magenta_bg": "\033[45m",
        "cyan_bg": "\033[46m",
        "white_bg": "\033[47m",
        "black_bright_bg": "\033[100m",  # bright background colors
        "red_bright_bg": "\033[101m",
        "green_bright_bg": "\033[102m",
        "yellow_bright_bg": "\033[103m",
        "blue_bright_bg": "\033[104m",
        "magenta_bright_bg": "\033[105m",
        "cyan_bright_bg": "\033[106m",
        "white_bright_bg": "\033[107m",
    }

    string = tags["reset"]

    for color in color_list:
        try:
            string += tags[color]
        except KeyError:
            print("Invalid color:", color)
            continue

    return string
