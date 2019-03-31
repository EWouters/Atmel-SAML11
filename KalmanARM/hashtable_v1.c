/*
 * hashtable.c
 *
 * Created: 2019-02-25 08:48:15
 *  Author: Dragos
 */ 

#include <math.h>
#include "../kalman.hpp"
#include "hashtable.h"

HASHTABLE_ITER_TYPE selectedIter = NOT_FOUND;

extern Kalman kalmanX; // Create the Kalman instances
extern Kalman kalmanY;

extern double accX, accY, accZ;
extern double gyroX, gyroY, gyroZ;

extern double roll, pitch;
extern double gyroXangle, gyroYangle; // Angle calculate using the gyro only
extern double compAngleX, compAngleY; // Calculated angle using a complementary filter
extern double kalAngleX, kalAngleY; // Calculated angle using a Kalman filter

struct hentry hashtab[HASHSIZE] = {{ 0 }};

unsigned char AreSame(double a, double b)
{
	if (fabs(a - b) < EPSILON) {
		return 0;
	}
	else {
		return 1;
	}
}

void hash() {
	unsigned int ax_ = ((unsigned int)(accX * MOD_PRECISION));
	//unsigned int ay_ = ((unsigned int)(accY * MOD_PRECISION)) % HASHSIZE;
	//unsigned int az_ = ((unsigned int)(accZ * MOD_PRECISION)) % HASHSIZE;
	
	unsigned int id = (ax_) % HASHSIZE;

	selectedIter = (HASHTABLE_ITER_TYPE) (hashtab+id);
}

void store() {
	selectedIter->accX = accX;
	selectedIter->accY = accY;
	selectedIter->accZ = accZ;
	selectedIter->gyroX = gyroX;
	selectedIter->gyroY = gyroY;
	selectedIter->gyroZ = gyroZ;
	selectedIter->roll = roll;
	selectedIter->pitch = pitch;
	selectedIter->gyroXangle = gyroXangle;
	selectedIter->gyroYangle = gyroYangle;
	selectedIter->compAngleX = compAngleX;
	selectedIter->compAngleY = compAngleY;
	selectedIter->kalAngleX = kalAngleX;
	selectedIter->kalAngleY = kalAngleY;
}

void lookup() {	
	hash();

	if (AreSame(accX, selectedIter->accX) == 1) {
		selectedIter = NOT_FOUND;
	}
	else if (AreSame(accY, selectedIter->accY) == 1) {
		selectedIter = NOT_FOUND;
	}
	else if (AreSame(accZ, selectedIter->accZ) == 1) {
		selectedIter = NOT_FOUND;
	}
	else if (AreSame(gyroX, selectedIter->gyroX) == 1) {
		selectedIter = NOT_FOUND;
	}
	else if (AreSame(gyroY, selectedIter->gyroY) == 1) {
		selectedIter = NOT_FOUND;
	}
	else if (AreSame(gyroZ, selectedIter->gyroZ) == 1) {
		selectedIter = NOT_FOUND;
	}
}
