IMPORTS=
SOURCE=qo.py
PREFIX=/usr/local/bin
LIBPREFIX=/usr/lib/qo
LIBS=libs/*
OUTPUT=dist/qo
PYI_FLAGS=$(addprefix --hidden-import ,$(IMPORTS)) -F

build:
	pyinstaller $(PYI_FLAGS) $(SOURCE)

winebuild: # Install PyInstaller: https://www.makeworld.space/2021/10/linux-wine-pyinstaller.html
	wine C:/Python310/Scripts/pyinstaller.exe $(PYI_FLAGS) $(SOURCE)

install: $(OUTPUT)
	cp $(OUTPUT) $(PREFIX)/qo
	rm -rf $(LIBPREFIX)
	mkdir -p $(LIBPREFIX)
	cp $(LIBS) $(LIBPREFIX)/

uninstall:
	rm -f $(PREFIX)/qo

clean:
	rm -rf build dist qo.spec __pycache__

docs:
	cd libs && python3 ../qdoc.py $(addsuffix .py,std date file qcf qo random stack string types) > ../docs.html
