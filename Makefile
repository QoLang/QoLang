SOURCE=qo.py
PREFIX=/usr/local/bin
OUTPUT=dist/qo

build:
	pyinstaller -F $(SOURCE)

install: $(OUTPUT)
	mv $(OUTPUT) $(PREFIX)/qo

uninstall:
	rm -f $(PREFIX)/qo

clean:
	rm -rf build dist qo.spec