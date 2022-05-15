# QoLang
A programming language, written in Python.

The project was inspired from [Let’s Build A Simple Interpreter.](https://ruslanspivak.com/lsbasi-part1/) article series.

## Installation
Currently not installable, but you can test it by cloning the repository and running `python3 qo.py file.qo`.

## Example
```
println("QoLang test");
println(""); | newline |
println("commands:");
println("  1  print 'Hello, world!'");
println("  2  print 'Hello, QoLang!'");
println("  3  print 'Hello, Camroku.TECH!'");
in := "";
input("> ", &in);
if (in == "1") { | note the ". "1" and 1 are not the same. |
  println("Hello, world!");
} else if (in == "2") {
  println("Hello, QoLang!");
} else if (in == "3") {
  println("Hello, Camroku.TECH!");
} else {
  println("Invalid input!");
};
```

Save this as `test.qo` (exists in repository with this content) and run `python3 qo.py test.qo`.