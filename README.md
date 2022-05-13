# QoLang
A programming language, written in Python.

The project was inspired from [Let’s Build A Simple Interpreter.](https://ruslanspivak.com/lsbasi-part1/) article series.

## Installation
Currently not installable, but you can test it by cloning the repository and running `python3 qo.py file.qo`.

## Examples
```
{
  println(1 == 1);
  out := "";
  input("> ", &out);
  println(out == "hello");
}
```

Save this as `test.qo` (exists in repository with this content) and run `python3 qo.py test.qo`.

This will print if `1` is equal to `1` (which is `True`) and wait for input with `> ` prompt, and will print if your input is equal to `"hello"` after the input. Note that this uses `println` and will print newline after the text, unlike `print`.