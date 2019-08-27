"""Contains a tool that detects whether a string is an integer."""


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

