"""
The date module implements basic date functions.
"""

import datetime
qolang_export = {
    "func_format": "format",
    "func_current": "current",
}


def func_format(Variables, args: list):
    """
    formatdate(date, format)

    Format UNIX timestamp.
    """
    return (Variables, datetime.datetime.utcfromtimestamp(args[0]).strftime(args[1]))


def func_current(Variables, args: list):
    """
    current()

    Get current date as UNIX timestamp.
    """
    return (Variables, datetime.datetime.now().timestamp())
