/*
 * kalman.c
 *
 * Created: 2019-02-11 12:11:03
 *  Author: Dragos
 */ 

#include "kalman.h"

void initializeKalman(Kalman *kalman) {
	/* We will set the variables like so, these can also be tuned by the user */
	kalman->Q_angle = 0.001;
	kalman->Q_bias = 0.003;
	kalman->R_measure = 0.03;

	kalman->angle = 0; // Reset the angle
	kalman->bias = 0; // Reset bias

	kalman->P[0][0] = 0; // Since we assume that the bias is 0 and we know the starting angle (use setAngle), the error covariance matrix is set like so - see: http://en.wikipedia.org/wiki/Kalman_filter#Example_application.2C_technical
	kalman->P[0][1] = 0;
	kalman->P[1][0] = 0;
	kalman->P[1][1] = 0;
}

double getAngle(Kalman *kalman, double newAngle, double newRate, double dt) {
	// KasBot V2  -  Kalman filter module - http://www.x-firm.com/?page_id=145
	// Modified by Kristian Lauszus
	// See my blog post for more information: http://blog.tkjelectronics.dk/2012/09/a-practical-approach-to-kalman-filter-and-how-to-implement-it

	// Discrete Kalman filter time update equations - Time Update ("Predict")
	// Update xhat - Project the state ahead
	/* Step 1 */
	kalman->rate = newRate - kalman->bias;
	kalman->angle += dt * kalman->rate;

	// Update estimation error covariance - Project the error covariance ahead
	/* Step 2 */
	kalman->P[0][0] += dt * (dt* kalman->P[1][1] - kalman->P[0][1] - kalman->P[1][0] + kalman->Q_angle);
	kalman->P[0][1] -= dt * kalman->P[1][1];
	kalman->P[1][0] -= dt * kalman->P[1][1];
	kalman->P[1][1] += kalman->Q_bias * dt;


	// Discrete Kalman filter measurement update equations - Measurement Update ("Correct")
	// Calculate Kalman gain - Compute the Kalman gain
	/* Step 4 */
	kalman->S = kalman->P[0][0] + kalman->R_measure;
	/* Step 5 */
	kalman->K[0] = kalman->P[0][0] / kalman->S;
	kalman->K[1] = kalman->P[1][0] / kalman->S;

	// Calculate angle and bias - Update estimate with measurement zk (newAngle)
	/* Step 3 */
	kalman->y = newAngle - kalman->angle;
	/* Step 6 */
	kalman->angle += kalman->K[0] * kalman->y;
	kalman->bias += kalman->K[1] * kalman->y;

	// Calculate estimation error covariance - Update the error covariance
	/* Step 7 */
	kalman->P[0][0] -= kalman->K[0] * kalman->P[0][0];
	kalman->P[0][1] -= kalman->K[0] * kalman->P[0][1];
	kalman->P[1][0] -= kalman->K[1] * kalman->P[0][0];
	kalman->P[1][1] -= kalman->K[1] * kalman->P[0][1];

	return kalman->angle;
};

void setAngle(Kalman *kalman, double newAngle) { kalman->angle = newAngle; }
void setQangle(Kalman *kalman, double newQ_angle) { kalman->Q_angle = newQ_angle; }
void setQbias(Kalman *kalman, double newQ_bias) { kalman->Q_bias = newQ_bias; }
void setRmeasure(Kalman *kalman, double newR_measure) { kalman->R_measure = newR_measure; };

double getQangle(Kalman *kalman) { return kalman->Q_angle; };
double getQbias(Kalman *kalman) { return kalman->Q_bias; };
double getRmeasure(Kalman *kalman) { return kalman->R_measure; };