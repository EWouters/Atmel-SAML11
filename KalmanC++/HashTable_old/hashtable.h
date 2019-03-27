/*
 * hashtable.h
 *
 * Created: 2019-02-25 09:26:59
 *  Author: Dragos
 */ 


#ifndef HASHTABLE_H_
#define HASHTABLE_H_

#define NOT_FOUND 0
#define HASHSIZE 120
#define EPSILON 0.5
#define MOD_PRECISION 100000
#define HASHTABLE_ITER_TYPE struct hentry*

struct hentry { /* table entry: */
	double accX;
	double accY;
	double accZ;
	double gyroX;
	double gyroY;
	double gyroZ;
	
	double roll;
	double pitch;
	double gyroXangle;
	double gyroYangle; // Angle calculate using the gyro only
	double compAngleX;
	double compAngleY; // Calculated angle using a complementary filter
	double kalAngleX;
	double kalAngleY;
};

extern struct hentry hashtab[HASHSIZE];

unsigned char AreSame(double a, double b);
void init();
void hash(); // the hash function
void store();
void lookup();

#endif /* HASHTABLE_H_ */
