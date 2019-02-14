/*
 * kalman_struct.h
 *
 * Created: 2019-02-11 14:03:06
 *  Author: Dragos
 */ 


#ifndef KALMAN_STRUCT_H_
#define KALMAN_STRUCT_H_

typedef struct Kalman_ {
	/* Kalman filter variables */
	double Q_angle; // Process noise variance for the accelerometer
	double Q_bias; // Process noise variance for the gyro bias
	double R_measure; // Measurement noise variance - this is actually the variance of the measurement noise

	double angle; // The angle calculated by the Kalman filter - part of the 2x1 state vector
	double bias; // The gyro bias calculated by the Kalman filter - part of the 2x1 state vector
	double rate; // Unbiased rate calculated from the rate and the calculated bias - you have to call getAngle to update the rate

	double P[2][2]; // Error covariance matrix - This is a 2x2 matrix
	double K[2]; // Kalman gain - This is a 2x1 vector
	double y; // Angle difference
	double S; // Estimate error
} Kalman;



#endif /* KALMAN_STRUCT_H_ */