/*
 * hashtable.h
 *
 * Created: 2019-02-25 09:26:59
 *  Author: Dragos
 */ 


#ifndef HASHTABLE_H_
#define HASHTABLE_H_

#define HASHSIZE 32
#define EPSILON 0.0001

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


static struct hentry hashtab[HASHSIZE];

int AreSame(double a, double b);
void init();
struct hentry *hash(double ax, double ay, double bx, double by);
void store(struct hentry *he, double i1x, double i1y, double i2x,  double i2y, double i3x, double i3y, double i4x, double i4y);
struct hentry *lookup(double ax, double ay, double az, double bx, double by, double bz);

#endif /* HASHTABLE_H_ */