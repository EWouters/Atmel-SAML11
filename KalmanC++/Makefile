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

kalman: $(SRC)/main.cpp $(SRC)/kalman.hpp
	g++ -m32 -Wall -I. -I$(SRC) -o kalman $(SRC)/main.cpp -lm

edit:
	vim kalman.cpp

clean:
	rm -f kalman *.o *~ output.csv
