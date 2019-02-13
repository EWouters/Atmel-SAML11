#
# Makefile for TinyEKF GPS example
#
# Copyright (C) 2015 Simon D. Levy
#
# MIT License

SRC = ${CURDIR}

all: kalman

run: kalman
	./kalman

kalman: $(SRC)/main.c $(SRC)/kalman.h
	g++ -Wall -I. -I$(SRC) -o kalman $(SRC)/main.c -lm

edit:
	vim kalman.c

clean:
	rm -f kalman *.o *~ output.csv
