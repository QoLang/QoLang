IMPORTS=
SOURCE=qo.py
PREFIX=/usr/local/bin
LIBPREFIX=/usr/lib/qo
LIBS=libs/*
OUTPUT=dist/qo

build:
	pyinstaller -F $(SOURCE) $(addprefix "--hidden-import ",$(IMPORTS))

winebuild: # Install PyInstaller: https://www.makeworld.space/2021/10/linux-wine-pyinstaller.html
	wine C:/Python310/Scripts/pyinstaller.exe -F $(SOURCE) $(addprefix "--hidden-import ",$(IMPORTS))

install: $(OUTPUT)
	cp $(OUTPUT) $(PREFIX)/qo
	rm -rf $(LIBPREFIX)
	mkdir -p $(LIBPREFIX)
	cp $(LIBS) $(LIBPREFIX)/

uninstall:
	rm -f $(PREFIX)/qo

clean:
	rm -rf build dist qo.spec