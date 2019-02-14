/*
 * printlines.c
 *
 * Created: 2019-02-11 12:13:21
 *  Author: Dragos
 */ 

#include <atmel_start.h>
#include "stdio_start.h"
#include "printlines.h"
#include "../globals.h"

int repeated_error = 0;
struct io_descriptor *io = 0;

void skipline() {
	char line[LINE_LENGTH];
	readline(line, LINE_LENGTH);
}

double stof (const char* s) {
	double rez = 0, fact = 1;
	if (*s == '-'){
		s++;
		fact = -1;
	};
	for (int point_seen = 0; *s; s++){
		if (*s == '.'){
			point_seen = 1;
			continue;
		};
		int d = *s - '0';
		if (d >= 0 && d <= 9){
			if (point_seen) fact /= 10.0f;
			rez = rez * 10.0f + (double)d;
		};
	};
	return rez * fact;
};

void readValues(double *valX, double *valY, double *valZ) {
	char line[LINE_LENGTH] = { '\0' };

	readline(line, LINE_LENGTH);
	//printline(line, LINE_LENGTH);
	
	int i = 0;
	int commas = 0;
	int comma_idx = 0;
	double* vals[3] = {valX, valY, valZ};
	
	char dbl[64] = { '\0' };

	while (commas < 4) {
		if (line[i] == ',' || line[i] == '\r' || line[i] == '\n' || line[i] == '\0') {
			dbl[i - comma_idx - 1] = '\0';
			comma_idx = i;
			
			if (commas == 0) {
				; // Do nothing and skip loop
			}
			else {
				*(vals[commas-1]) = stof(dbl);
			}
			commas++;
		}
		else /* line[i] != ',' */ {
			if (commas > 0) {
				dbl[i - comma_idx - 1] = line[i];
			}
		}
		i++;
	}
}

int readline_(char* line, int length) {
	char c = '1';
	int index = 0;
	int not_ok = 1;
	
	while (c != '\n') {
		if (index >= (length - 2)) break;
		
		if (line[index] == '\r') {
			index++;
			continue;
		}
		
		stdio_io_read((uint8_t *)(&c), 1);
		line[index++] = c;
		//delay_ms(1);
		
		if (c > '\r') not_ok = 0;
	}
	line[index] = '\0';
	
	if (index < 1) return 1;
	
	return not_ok;
}

void readline(char* line, int length) {
	char temp[256] = { '\0' };
	while(temp[0] != 'k') { // "k" from "ok"
		while (readline_(line, length) == 1);
		printline(line, length);
		while (readline_(temp, 256) == 1);
		if ((temp[0] >= '0') && (temp[0] <= '9')) {
			printf("f");
		}
		if ((temp[0] != 'k') && (temp[0] != 'r')) {
			printf("b\n");
		}
	}
}

void printline(char *line, int length) {
	int index = 0;
	char c;
	
	while ((line[index] != '\0') && (line[index] != '\n') && (line[index] != '\r')) {
		if ( index >= (length-2) ) break;
		
		stdio_io_write((uint8_t*)(&(line[index++])), 1);
		//delay_ms(1);
	}
	
	c = '\r';
	stdio_io_write((uint8_t*)(&c), 1);
	c = '\n';
	stdio_io_write((uint8_t*)(&c), 1);
}

// for every increment in accuracy you get 6 digits
void printDouble(double dbl, int accuracy) {
	int dblSign = (dbl < 0) ? -1 : 1;
	dbl = (dbl < 0) ? -dbl : dbl;
	
	unsigned long int tmpInt = dbl; // Get the integer side
	
	if (dblSign < 0) {
		printf("-%lu.", tmpInt); // Print sign and integer
	}
	else {
		printf("%lu.", tmpInt); // Print sign and integer
	}
	
	int i;
	for (i=0; i<accuracy; i++) {
		dbl = dbl - tmpInt; // Get the fraction
		tmpInt = dbl * 1000000; // Turn fraction to integer
		dbl  = dbl * 1000000;
		
		printf("%06lu", tmpInt); // Print fraction
	}
}

void printValues(double valX, double valY, double valZ) {
	printDouble(valX, 2);
	printf(",");
	printDouble(valY, 2);
	printf(",");
	printDouble(valZ, 2);
	printf("\r\n");
}

void printValuesExtended(int idx, double roll, double pitch, double gyroXangle, double gyroYangle, double compAngleX, double compAngleY, double kalAngleX, double kalAngleY) {
	printf("%d,", idx);
	printDouble(roll, 1);
	printf(",");
	printDouble(pitch, 1);
	printf(",");
	printDouble(gyroXangle, 1);
	printf(",");
	printDouble(gyroYangle, 1);
	printf(",");
	printDouble(compAngleX, 1);
	printf(",");
	printDouble(compAngleY, 1);
	printf(",");
	printDouble(kalAngleX, 1);
	printf(",");
	printDouble(kalAngleY, 1);
	printf("\n");
}