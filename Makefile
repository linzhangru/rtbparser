.PHONY : all


all :
	gcc -o rtbp rtbp.c
install: rtbp
	@sudo cp rtbp     /usr/bin/rtbp
	@sudo cp rtbps.py /usr/bin/rtbps
	@sudo chmod 755 /usr/bin/rtbp
	@sudo chmod 755 /usr/bin/rtbps
