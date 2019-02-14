/*
 * kalman_globals.h
 *
 * Created: 2019-02-11 12:49:24
 *  Author: Dragos
 */ 


#ifndef KALMAN_GLOBALS_H_
#define KALMAN_GLOBALS_H_

#define RAD_TO_DEG 57.295779513082321

#define RESTRICT_PITCH // Comment out to restrict roll to ±90deg instead
// please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf

double accX, accY, accZ;
double gyroX, gyroY, gyroZ;

#endif /* KALMAN_GLOBALS_H_ */