/*
 * main.h
 *
 * Created: 2019-02-11 11:44:31
 *  Author: Dragos
 */ 

#ifndef MAIN_H_
#define MAIN_H_

// Source: https://github.com/TKJElectronics/KalmanFilter

#include "Kalman/kalman_struct.h"

#define LINE_LENGTH 256

#define DO_DELAY
#define DELAY_DURATION 1000

Kalman kalmanX; // Create the Kalman instances
Kalman kalmanY;

double gyroXangle;
double gyroYangle; // Angle calculate using the gyro only
double compAngleX;
double compAngleY; // Calculated angle using a complementary filter
double kalAngleX;
double kalAngleY; // Calculated angle using a Kalman filter



#endif /* MAIN_H_ */