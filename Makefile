SHELL    = /bin/bash

DEVICE   ?= /dev/ttyUSB0
DST      ?= /flash

all:

copy: F ?= ""
copy:
	@if [ -z "$(F)" ]; then echo "Use: make copy F=file";\
	else \
		rshell -d -p $(DEVICE) cp "$(F)" $(DST)/$(F) \
		| grep "^output = re"; \
	fi

serial-monitor:
	@echo "ctrl+a + ctrl+q to exit"
	picocom $(DEVICE) -b 115200

shell:
	rshell -p $(DEVICE)
