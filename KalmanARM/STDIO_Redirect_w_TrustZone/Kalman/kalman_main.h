/*
 * kalman_main.h
 *
 * Created: 2019-02-11 12:20:19
 *  Author: Dragos
 */ 


#ifndef KALMAN_MAIN_H_
#define KALMAN_MAIN_H_

#include "kalman_globals.h"
#include "globals.h"

void skipline();
void readValues(double *accX, double *accY, double *accZ);
//void readGyro(double *gyroX, double *gyroY, double *gyroZ);

void loop(int idx);

#endif /* KALMAN_MAIN_H_ */