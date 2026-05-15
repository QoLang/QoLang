IMPORTS=sqlite3
SOURCE=qo.py
PREFIX=/usr/local/bin
LIBPREFIX=/usr/lib/qo
# fix these if your wine prefix is different
WINEPREFIX=$(HOME)/.wine/drive_c/qolang
WINELIBPREFIX=$(HOME)/.wine/drive_c/qolang/libs
LIBS=libs/*
OUTPUT=dist/qo
PYI_FLAGS=$(addprefix --hidden-import ,$(IMPORTS)) -F
WINEPYTHONDIR=C:/Python314

TRIMMED_WINEDIR := $(strip $(WINEPREFIX))

.PHONY: build clean install uninstall winebuild docs

build:
	pyinstaller $(PYI_FLAGS) $(SOURCE)

winebuild: # Install PyInstaller: https://www.makeworld.space/2021/10/linux-wine-pyinstaller.html
	wine $(WINEPYTHONDIR)/Scripts/pyinstaller.exe $(PYI_FLAGS) $(SOURCE)

install: $(OUTPUT)
	cp $(OUTPUT) $(PREFIX)/qo
	rm -rf $(LIBPREFIX)
	mkdir -p $(LIBPREFIX)
	cp $(LIBS) $(LIBPREFIX)/

wineinstall: $(OUTPUT).exe
	echo "Temizlenmiş Yol: $(TRIMMED_WINEDIR)"
	mkdir -p $(WINELIBPREFIX)
	cp $(OUTPUT).exe $(WINELIBPREFIX)/qo.exe
	cp $(LIBS) $(WINELIBPREFIX)/

uninstall:
	rm -f $(PREFIX)/qo

clean:
	rm -rf build dist qo.spec __pycache__

docs:
	cd libs && python3 ../qdoc.py $(addsuffix .py,std date file qcf qo random stack string types) > ../docs.html
