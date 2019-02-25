/*
 * printlines.h
 *
 * Created: 2019-02-11 12:12:25
 *  Author: Dragos
 */ 


#ifndef PRINTLINES_H_
#define PRINTLINES_H_

extern int repeated_error;
extern struct io_descriptor *io;

void skipline();
double stof (const char* s);
void readValues(double *accX, double *accY, double *accZ);
int readline_(char* line, int length);
void readline(char* line, int length);
void printline(char *line, int length);
void printDouble(double dbl, int accuracy);
void printValues(double valX, double valY, double valZ);
void printValuesExtended(int idx, double roll, double pitch, double gyroXangle, double gyroYangle, double compAngleX, double compAngleY, double kalAngleX, double kalAngleY);
#endif /* PRINTLINES_H_ */