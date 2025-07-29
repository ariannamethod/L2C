
# choose your compiler, e.g. gcc/clang
CC = gcc

.PHONY: clean
clean:
rm -f libl2c.so

.PHONY: lib
lib: l2c.c
	$(CC) -Ofast -fPIC -shared -o libl2c.so l2c.c -lm
