/*
 * printlines.c
 *
 * Created: 2019-02-11 12:13:21
 *  Author: Dragos
 */ 

#include <atmel_start.h>
#include "stdio_start.h"
#include "printlines.h"
#include <stdint.h>
#include <tgmath.h>

int repeated_error = 0;
struct io_descriptor *io = 0;

int readline_(char* line, int length) {
	char c = '1';
	int index = 0;
	int not_ok = 1;
	
	while (c != '\n') {
		if ( index >= (length - 2)) break;
		
		if (line[index] == '\r') continue;
		
		stdio_io_read((uint8_t *)(&c), 1);
		line[index++] = c;
		
		if (c > '\r') not_ok = 0;
	}
	line[index] = '\0';
	
	return not_ok;
}

void readline(char* line, int length) {
	while (readline_(line, length) == 1);
}

void printline(char *line, int length) {
	int index = 0;
	char c;
	
	while ((line[index] != '\0') && (line[index] != '\n') && (line[index] != '\r')) {
		if ( index >= (length-2) ) break;
		
		stdio_io_write((uint8_t*)(&(line[index++])), 1);
		delay_ms(1);
	}
	
	c = '\r';
	stdio_io_write((uint8_t*)(&c), 1);
	c = '\n';
	stdio_io_write((uint8_t*)(&c), 1);
}

// accuracy times 2 = how many digits do you want after the (.)
void printDouble(double dbl, int accuracy) {
	char *tmpSign = (dbl < 0) ? "-" : "";
	dbl = (dbl < 0) ? -dbl : dbl;
	
	unsigned long int tmpInt = dbl; // Get the integer side
	
	printf("%s%lu.", tmpSign, tmpInt); // Print sign and integer
	
	int i;
	for (i=0; i<accuracy; i++) {
		dbl = dbl - tmpInt; // Get the fraction
		tmpInt = dbl * 1000000000; // Turn fraction to integer
		dbl  = dbl * 1000000000;
		
		printf("%09lu", tmpInt); // Print fraction
	}
}

void printValues(double valX, double valY, double valZ) {
	printDouble(valX, 2);
	printf(",");
	printDouble(valY, 2);
	printf(",");
	printDouble(valZ, 2);
	printf("\n");
}

void printValuesExtended(int idx, double roll, double pitch, double gyroXangle, double gyroYangle, double compAngleX, double compAngleY, double kalAngleX, double kalAngleY) {
	printf("%d,", idx);
	printDouble(roll, 2);
	printf(",");
	printDouble(pitch, 2);
	printf(",");
	printDouble(gyroXangle, 2);
	printf(",");
	printDouble(gyroYangle, 2);
	printf(",");
	printDouble(compAngleX, 2);
	printf(",");
	printDouble(compAngleY, 2);
	printf(",");
	printDouble(kalAngleX, 2);
	printf(",");
	printDouble(kalAngleY, 2);
	printf("\n");
}