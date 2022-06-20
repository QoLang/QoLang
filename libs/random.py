# QoLang Standart Library - random.py
import random

qolang_export = {
    "func_range": "range",
    "func_int": "int",
    "func_choice": "choice",
    "func_shuffle": "shuffle",
}


def func_range(Variables, args: list):
    """
    Return a randomly selected element from range(start, stop, step).
    """
    output = random.randrange(args[0], args[1], args[2])
    return (Variables, output)


def func_int(Variables, args: list):
    """
    Alias for random.range(a, b+1, 1);
    """
    output = random.randint(args[0], args[1])
    return (Variables, output)


def func_choice(Variables, args: list):
    """
    Return a random element from a non-empty list.
    """
    output = random.choice(args[0])
    return (Variables, output)


def func_shuffle(Variables, args: list):
    """
    Shuffle a list.
    """
    output = random.sample(args[0], k=len(args[0]))
    return (Variables, output)
