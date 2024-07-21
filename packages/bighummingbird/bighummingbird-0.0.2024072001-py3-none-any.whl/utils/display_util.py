import sys

def clear_line():
    """
    Clears the current console line using a carriage return and space padding.
    Adjust the padding length if needed to cover longer lines.
    """
    # Move the cursor back to the beginning of the line
    sys.stdout.write('\r')
    # Overwrite the line with spaces
    sys.stdout.write(' ' * 80)  # Assuming 80 characters is the width of your console
    # Move the cursor back to the beginning again
    sys.stdout.write('\r')

def green_check():
    """
    Prints a green check mark in the console.
    """
    # ANSI escape code for green text
    green_color = '\033[92m'
    # Unicode character for check mark
    check_mark = '\u2714'

    # Print the check mark in green
    return green_color + check_mark

def red_check():
    # ANSI escape code for red text
    red_color = '\033[91m'
    # ANSI escape code to reset color to default
    reset_color = '\033[0m'
    # Unicode character for "X"
    x_mark = '\u2716'

    # Print the "X" in red
    return red_color + x_mark

def orange_exclamation():
    # ANSI escape code for orange text
    orange_color = '\033[38;2;255;165;0m'  # 38;5;208 is the ANSI code for orange

    # Unicode character for "!"
    exclamation_mark = '\u2757'

    # Print the exclamation mark in orange
    return orange_color + exclamation_mark

def bold():
    # ANSI escape code for bold text
    bold_text = '\033[1m'
    return bold_text

def reset_font():
    reset_text = '\033[22m'
    return reset_text

def right_angle():
    right_angle = '\u221F'
    return right_angle

def orange():
    # ANSI escape code for orange text
    orange_color = '\033[38;5;208m'  # 38;5;208 is the ANSI code for orange
    return orange_color

def gray():
    # ANSI escape code for gray text
    gray_color = '\033[90m'
    return gray_color

def reset_color():
    reset_color = '\033[0m'
    return reset_color

def blue():
    blue_color = '\033[38;5;27m'
    return blue_color

def blue_underline(url):
    blue_underline_color = f"\033[4;38;5;27m{url}\033[0m"
    return blue_underline_color