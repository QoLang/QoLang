"""
The types module contains functions for working with types.
"""

qolang_export = {
    "func_toInt": "toInt",
    "func_toBool": "toBool",
    "func_toStr": "toStr",
    "func_toFloat": "toFloat",
    "func_dictValues": "dictValues",
    "func_dictKeys": "dictKeys",
    "func_dictItems": "dictItems",
    "func_type": "type",
}


def func_toInt(Variables, args: list):
    """
    types.toInt(variable)

    Convert any type of variable to Int.
    """
    out = 0
    if type(args[0]) in [int, float]:
        out = int(args[0])
    elif type(args[0]) == str:
        try:
            out = int(args[0], 0)
        except:
            out = 0 if args[0] == "" else 1
    elif type(args[0]) == bool:
        out = 1 if args[0] else 0

    return (Variables, out)


def func_toBool(Variables, args: list):
    """
    types.toBool(variable)

    Convert any type of variable to Bool.
    """
    out = False
    if type(args[0]) in [int, float]:
        out = args[0] == 1
    elif type(args[0]) == str:
        out = args[0] != ""
    elif type(args[0]) == bool:
        out = out

    return (Variables, out)


def func_toStr(Variables, args: list):
    """
    types.toStr(variable)

    Convert any type of variable to Str.
    """
    out = str(args[0])
    return (Variables, out)


def func_toFloat(Variables, args: list):
    """
    types.toFloat(variable)

    Convert any type of variable to Float.
    """
    out = 0.0
    if type(args[0]) in [int, float]:
        out = float(args[0])
    elif type(args[0]) == str:
        try:
            out = float(args[0])
        except:
            out = 0.0 if args[0] == "" else 1.0
    elif type(args[0]) == bool:
        out = 1.0 if args[0] else 0.0

    return (Variables, out)


def func_dictValues(Variables, args: list):
    """
    types.dictValues(dictionary)

    Get values of a dictionary as a List.
    """
    out = []
    if type(args[0]) == dict:
        out = list(args[0].values())

    return (Variables, out)


def func_dictKeys(Variables, args: list):
    """
    types.dictValues(dictionary)

    Get keys of a dictionary as a List.
    """
    out = []
    if type(args[0]) == dict:
        out = list(args[0].keys())

    return (Variables, out)


def func_dictItems(Variables, args: list):
    """
    types.dictItems(dictionary)

    Get items of a dictionary as two Lists.
    """
    out = []
    if type(args[0]) == dict:
        out = [list(args[0].keys()), list(args[0].values())]

    return (Variables, out)


def func_type(Variables, args: list):
    """
    types.type(variable)

    Get type of something.
    """
    types = {
        int: "Int",
        str: "Str",
        bool: "Bool",
        float: "Float",
        dict: "Dict",
    }
    out = types.get(type(args[0]), type(args[0]))
    return (Variables, out)
