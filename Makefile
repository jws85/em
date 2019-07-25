PREFIX=/usr/local

install:
	@echo "Installing em to ${PREFIX}..."
	mkdir -p ${PREFIX}/bin
	mkdir -p ${PREFIX}/share/em
	cp em ${PREFIX}/bin
	cp em.conf ${PREFIX}/share/em
	cp loading.gif ${PREFIX}/share/em
	@echo "done!"

uninstall:
	@echo "Uninstalling em from ${PREFIX}..."
	rm -f ${PREFIX}/bin/em
	rm -rf ${PREFIX}/share/em
	@echo "done!"
