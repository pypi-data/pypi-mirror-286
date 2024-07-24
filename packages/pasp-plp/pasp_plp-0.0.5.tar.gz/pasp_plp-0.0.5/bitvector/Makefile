CC=gcc
CFLAGS=-Wall -Wextra -pedantic
UCFLAGS=
DEBUG=

main: bitvector tests
	$(CC) $(UCFLAGS) $(CFLAGS) $(DEBUG) -o a.out bitvector.o tests.o

debug: DEBUG += -g
debug: main

bitvector: bitvector.c bitvector.h
	$(CC) $(UCFLAGS) $(CFLAGS) $(DEBUG) -c bitvector.c

tests:
	$(CC) $(UCFLAGS) $(CFLAGS) $(DEBUG) -c tests.c

clean:
	rm -f *.o *.out *.h.gch
