# QoLang version 0.1
The Qo Programming Language, or QoLang.

The project was inspired from [Let’s Build A Simple Interpreter.](https://ruslanspivak.com/lsbasi-part1/) article series.

## Installation
### Latest Release (more stable, less features)
Please refer to the [website](https://qolang.camroku.tech/#Installation).

### Latest Commit (less stable, more features)
You need `make` and `pyinstaller`.

Run this command as root:
```
make clean build install
```

To uninstall, run this command as root:
```
make uninstall
```

A custom installer will be made in the future, with Windows support.

## Example
For an example, see `test.qo`.