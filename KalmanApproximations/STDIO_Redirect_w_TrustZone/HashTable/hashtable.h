/*
 * hashtable.h
 *
 * Created: 2019-02-25 09:26:59
 *  Author: Dragos
 */ 


#ifndef HASHTABLE_H_
#define HASHTABLE_H_

int AreSame(double a, double b);
void init();
struct hentry *hash(double ax, double ay, double bx, double by);
void store(struct hentry *he, double i1x, double i1y, double i1z,  double i2x, double i2y, double i2z);
struct hentry *lookup(double ax, double ay, double az, double bx, double by, double bz);



#endif /* HASHTABLE_H_ */