#
# Makefile for TinyEKF GPS example
#
# Copyright (C) 2015 Simon D. Levy
#
# MIT License

SRC = ${CURDIR}

# hash-exp: hash_experiment
#	gcc -m32 -g -Wall hash_experiment.c -o hash_experiment

run-kalman-hash: kalman-hash
	./kalman-hash

run-kalman: kalman
	./kalman

kalman: $(SRC)/main.cpp $(SRC)/kalman.hpp clean-kalman
	g++ -m32 -g -Wall -I. -I$(SRC) -o kalman $(SRC)/main.cpp -lm -O0

kalman-hash: $(SRC)/main_hash.cpp $(SRC)/kalman.hpp $(SRC)/HashTable/hashtable.c $(SRC)/HashTable/hashtable.h clean-kalman-hash
	g++ -m32 -g -Wall -I. -I$(SRC) -I$(SRC)/HashTable/ -o kalman-hash $(SRC)/main_hash.cpp $(SRC)/HashTable/hashtable.c -lm -O0

clean-kalman:
	rm -f kalman *.o *~

clean-kalman-hash:
	rm -f kalman-hash *.o *~


