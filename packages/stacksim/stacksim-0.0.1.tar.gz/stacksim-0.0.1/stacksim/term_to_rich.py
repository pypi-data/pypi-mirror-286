from termcolor import colored
from rich.console import Console
from rich.text import Text


# Function to convert termcolor to rich markup
def termcolor_to_rich_markup(termcolor_str):
    color_map = {
        'grey': 'gray',
        'red': 'red',
        'green': 'green',
        'yellow': 'yellow',
        'blue': 'blue',
        'magenta': 'magenta',
        'cyan': 'cyan',
        'white': 'white',
        'dark_grey': 'grey53',
        'dark_red': 'maroon',
        'dark_green': 'dark green',
        'dark_yellow': 'olive',
        'dark_blue': 'navy',
        'dark_magenta': 'purple',
        'dark_cyan': 'teal',
        'dark_white': 'silver'
    }

    parts = termcolor_str.split('\x1b[')
    rich_markup = ""

    for part in parts:
        if 'm' in part:
            code, text = part.split('m', 1)
            if code == '0':
                rich_markup += text
            else:
                try:
                    color_code = int(code.split(';')[0])
                    color = {
                        30: 'grey',
                        31: 'red',
                        32: 'green',
                        33: 'yellow',
                        34: 'blue',
                        35: 'magenta',
                        36: 'cyan',
                        37: 'white',
                        90: 'dark_grey',
                        91: 'dark_red',
                        92: 'dark_green',
                        93: 'dark_yellow',
                        94: 'dark_blue',
                        95: 'dark_magenta',
                        96: 'dark_cyan',
                        97: 'dark_white',
                    }.get(color_code, None)
                    rich_color = color_map.get(color, None)
                    if rich_color:
                        rich_markup += f"[{rich_color}]{text}[/{rich_color}]"
                    else:
                        rich_markup += text
                except ValueError:
                    rich_markup += '\x1b[' + part
        else:
            rich_markup += part

    return rich_markup

