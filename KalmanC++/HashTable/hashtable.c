/*
 * hashtable.c
 *
 * Created: 2019-02-25 08:48:15
 *  Author: Dragos
 */ 

#include <math.h>
#include "hashtable.h"

int AreSame(double a, double b)
{
	if (fabs(a - b) < EPSILON) {
		return 0;
	}
	else {
		return -1;
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
struct hentry *hash(double ax, double ay, double bx, double by) {
	//unsigned int ax_ = (int)(ax * MOD_PRECISION) % HASHSIZE;
	unsigned int ay_ = (int)(ay * MOD_PRECISION) % HASHSIZE;
	//unsigned int bx_ = fmod((bx * MOD_PRECISION), HASHSIZE);
	//unsigned int by_ = fmod((by * MOD_PRECISION), HASHSIZE);
	
	//unsigned int id = (ax_ + ay_) % HASHSIZE;
	

	return &(hashtab[ay_]);
}

void store(struct hentry *he, double i1x, double i1y, double i2x,  double i2y, double i3x, double i3y, double i4x, double i4y) {
	he->roll = i1x;
	he->pitch = i1y;
	he->gyroXangle = i2x;
	he->gyroYangle = i2y;
	he->compAngleX = i3x;
	he->compAngleY = i3y;
	he->kalAngleX = i4x;
	he->kalAngleY = i4y;
}

/* lookup: look for s in hashtab */
struct hentry *lookup(double ax, double ay, double az, double bx, double by, double bz) {	
	struct hentry *he = hash(ax, ay, bx, by);
	
	if (AreSame(ax, he->accX) != -1) {
		return (struct hentry*) nullptr;
	}
	
	if (AreSame(ay, he->accY) == -1) {
		return (struct hentry*) nullptr;
	}
	
	if (AreSame(az, he->accZ) == -1) {
		return (struct hentry*) nullptr;
	}
	
	if (AreSame(bx, he->gyroX) == -1) {
		return (struct hentry*) nullptr;
	}
	
	if (AreSame(by, he->gyroY) == -1) {
		return (struct hentry*) nullptr;
	}
	
	if (AreSame(bz, he->gyroZ) == -1) {
		return (struct hentry*) nullptr;
	}
	
	return he;
}