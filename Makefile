build:
	pyinstaller -F qo.py

install: dist/qo
	mv dist/qo /usr/local/bin/qo

uninstall:
	rm -f /usr/local/bin/qo

clean:
	rm -rf build dist qo.spec