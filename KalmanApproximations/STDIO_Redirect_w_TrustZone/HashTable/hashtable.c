/*
 * hashtable.c
 *
 * Created: 2019-02-25 08:48:15
 *  Author: Dragos
 */ 

#include <math.h>

struct hentry { /* table entry: */
	double kalAngleX;
	double kalAngleY;
	double kalAngleZ;
	double gyroAngleX;
	double gyroAngleY;
	double gyroAngleZ;
	double gyroXangle;
	double gyroYangle; // Angle calculate using the gyro only
	double compAngleX;
	double compAngleY; // Calculated angle using a complementary filter
};

#define HASHSIZE 4
#define EPSILON 0.000001
static struct hentry hashtab[HASHSIZE][HASHSIZE][HASHSIZE][HASHSIZE];

int AreSame(double a, double b)
{
	return fabs(a - b) < EPSILON;
}

void init() {
	int a = 0, b = 0, c = 0, d = 0;
	
	for (a = 0; a < HASHSIZE; a++) {
		for (b = 0; b < HASHSIZE; b++) {
			for (c = 0; c < HASHSIZE; b++) {
				for (d = 0; d < HASHSIZE; d++) {
					hashtab[a][b][c][d].kalAngleX = -1;
					hashtab[a][b][c][d].kalAngleY = -1;
					hashtab[a][b][c][d].kalAngleZ = -1;
					hashtab[a][b][c][d].gyroAngleX = -1;
					hashtab[a][b][c][d].gyroAngleY = -1;
					hashtab[a][b][c][d].gyroAngleZ = -1;
					hashtab[a][b][c][d].gyroXangle = -1;
					hashtab[a][b][c][d].gyroYangle = -1;
					hashtab[a][b][c][d].compAngleX = -1;
					hashtab[a][b][c][d].compAngleY = -1;
				}
			}
		}
	}
}

/* hash: form hash value for double d*/
struct hentry *hash(double ax, double ay, double bx, double by) {
	unsigned int ax_ = fmod(ax, HASHSIZE);
	unsigned int ay_ = fmod(ay, HASHSIZE);
	unsigned int bx_ = fmod(bx, HASHSIZE);
	unsigned int by_ = fmod(by, HASHSIZE);
	
	return &(hashtab[ax_][ay_][bx_][by_]);
}

void store(struct hentry *he, double i1x, double i1y, double i1z,  double i2x, double i2y, double i2z) {
	he->kalAngleX = i1x;
	he->kalAngleY = i1y;
	he->kalAngleZ = i1z;
	he->gyroAngleX = i2x;
	he->gyroAngleY = i2y;
	he->gyroAngleZ = i2z;
}

/* lookup: look for s in hashtab */
struct hentry *lookup(double ax, double ay, double az, double bx, double by, double bz) {	
	struct hentry *hpoint = hash(ax, ay, bx, by);
	
	int ok = 1;
	
	if (az != hpoint->kalAngleZ) {
		ok = 0;
	}
	
	if (bz != hpoint->gyroAngleZ) {
		ok = 0;
	}
	
	if (ok == 1) {
		return hpoint;
	}
	else {
		return (struct hentry*) -1;
	}
}