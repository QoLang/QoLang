# QoLang
A programming language, written in Python.

The project was inspired from [Let’s Build A Simple Interpreter.](https://ruslanspivak.com/lsbasi-part1/) article series.

## Installation
Currently not installable, but you can test it by cloning the repository and running `python3 qo.py file.qo`.

## Examples
```
{
  input("> ", toprint);
  println(toprint, "this looks nice!");
}
```

Save this as `test.qo` (exists in repository with this content) and run `python3 qo.py test.qo`.

This will print `> ` and wait for input, and will print `input this looks nice!` (where `input` is the input you've entered) after the input. Note that this uses `println` and will print newline after the text, unlike `print`.