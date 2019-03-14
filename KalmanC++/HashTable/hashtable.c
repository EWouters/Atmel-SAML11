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

// void init() {
// 	int a = 0;
	
// 	for (a = 0; a < HASHSIZE; a++) {
// 		hashtab[a].accX = -1;
// 		hashtab[a].accY = -1;
// 		hashtab[a].accZ = -1;
// 		hashtab[a].gyroX = -1;
// 		hashtab[a].gyroY = -1;
// 		hashtab[a].gyroZ = -1;
// 		hashtab[a].roll = -1;
// 		hashtab[a].pitch = -1;
// 		hashtab[a].gyroXangle = -1;
// 		hashtab[a].gyroYangle = -1;
// 		hashtab[a].compAngleX = -1;
// 		hashtab[a].compAngleY = -1;
// 		hashtab[a].kalAngleX = -1;
// 		hashtab[a].kalAngleY = -1;
// 	}
// }

/* hash: form hash value for double d*/
void hash() {
	unsigned int ax_ = ((unsigned int)(accX * MOD_PRECISION)) % HASHSIZE;
	unsigned int ay_ = ((unsigned int)(accY * MOD_PRECISION)) % HASHSIZE;
	//unsigned int bx_ = fmod((bx * MOD_PRECISION), HASHSIZE);
	//unsigned int by_ = fmod((by * MOD_PRECISION), HASHSIZE);
	
	unsigned int id = (ax_ + ay_) % HASHSIZE;

	selectedIter = (HASHTABLE_ITER_TYPE) (hashtab+id);
}

void store() {
	// hashtab[i].accX = accX;
	// hashtab[i].accY = accY;
	// hashtab[i].accZ = accZ;
	// hashtab[i].gyroX = gyroX;
	// hashtab[i].gyroY = gyroY;
	// hashtab[i].gyroZ = gyroZ;
	// hashtab[i].roll = roll;
	// hashtab[i].pitch = pitch;
	// hashtab[i].gyroXangle = gyroXangle;
	// hashtab[i].gyroYangle = gyroYangle;
	// hashtab[i].compAngleX = compAngleX;
	// hashtab[i].compAngleY = compAngleY;
	// hashtab[i].kalAngleX = kalAngleX;
	// hashtab[i].kalAngleY = kalAngleY;
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

/* lookup: look for s in hashtab */
void lookup() {	
	hash();
	
	// if (AreSame(ax, hashtab[idx].accX) == -1) {
	// 	return NOT_FOUND;
	// }
	
	// if (AreSame(ay, hashtab[idx].accY) == -1) {
	// 	return NOT_FOUND;
	// }
	
	// if (AreSame(az, hashtab[idx].accZ) == -1) {
	// 	return NOT_FOUND;
	// }
	
	// if (AreSame(bx, hashtab[idx].gyroX) == -1) {
	// 	return NOT_FOUND;
	// }
	
	// if (AreSame(by, hashtab[idx].gyroY) == -1) {
	// 	return NOT_FOUND;
	// }
	
	// if (AreSame(bz, hashtab[idx].gyroZ) == -1) {
	// 	return NOT_FOUND;
	// }

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