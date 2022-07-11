# QoLang
The Qo Programming Language, or QoLang.

The project was inspired from [Let’s Build A Simple Interpreter.](https://ruslanspivak.com/lsbasi-part1/) article series.

## Installation
### Latest Release (more stable, less features)
Please refer to the [website](https://qolang.camroku.tech/#Install).

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

If you need other Python libraries in QoLang (like requests), you can add them as a space-seperated list to `IMPORTS` variable in Makefile.

## Example
For an example, see the `example` directory.