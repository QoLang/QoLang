# QoLang
A programming language, written in Python.

The project was inspired from [Let’s Build A Simple Interpreter.](https://ruslanspivak.com/lsbasi-part1/) article series.

## Installation
Currently not installable, but you can test it by cloning the repository and running `python3 qo.py file.qo`.

## Examples
```
println(1 == 1); | print if 1 is equal to 1 (True) |
out := ""; | initialize variable `out` |
input("> ", &out); | get input to the variable `out` |
println(out == "hello"); | print if the variable `out` is equal to "hello" |
```

Save this as `test.qo` (exists in repository with this content) and run `python3 qo.py test.qo`.