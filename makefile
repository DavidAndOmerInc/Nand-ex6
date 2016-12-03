TARGETS = Assembler

all: $(TARGETS)

Assembler: Main.py
	cp -f $< $@
	chmod +x $@