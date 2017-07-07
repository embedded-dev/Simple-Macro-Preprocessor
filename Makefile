PROGRAM = smp
DEST_DIR = /usr/local/bin

all : ${PROGRAM}

./${PROGRAM} : ${PROGRAM}.py
	/bin/cp -a $< $@

install : ${DEST_DIR}/${PROGRAM}

${DEST_DIR}/${PROGRAM} : ./${PROGRAM}
	/bin/cp -a $< $@

test : ./${PROGRAM} wifi.h-updated

wifi.h-updated : wifi.json wifi.h
	./${PROGRAM} -m wifi.json wifi.h > $@ && echo "Header test successful"

clean :
	${RM} ./${PROGRAM} ./*-updated
