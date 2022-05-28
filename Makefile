SOURCE=qo.py
PREFIX=/usr/local/bin
LIBPREFIX=/usr/lib/qo
LIBS=libs/*
OUTPUT=dist/qo

build:
	pyinstaller -F $(SOURCE)

install: $(OUTPUT)
	cp $(OUTPUT) $(PREFIX)/qo
	mkdir -p $(LIBPREFIX)
	cp $(LIBS) $(LIBPREFIX)/

uninstall:
	rm -f $(PREFIX)/qo

clean:
	rm -rf build dist qo.spec