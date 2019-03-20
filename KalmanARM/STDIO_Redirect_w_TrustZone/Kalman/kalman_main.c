/*
 * kalman_main.c
 *
 * Created: 2019-02-11 12:20:03
 *  Author: Dragos
 */ 

#include <atmel_start.h>
#include <tgmath.h>
//#include "../Measurements/measurements.h"
#include "../globals.h"
#include "kalman.h"
#include "kalman_main.h"
//#include "kalman_globals.h"
#include "stdio_start.h"
//#include "globals.h"
#include "../PrintLines/printlines.h"

double abs2(double val) {
	if (val < 0) {
		return -val;
	}
	else {
		return val;
	}
}

void loop(int idx) {
	//char output[LINE_LENGTH] = { '\n' };

	double dt = 1; // Calculate delta time

	// Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
	// atan2 outputs the value of -? to ? (radians) - see http://en.wikipedia.org/wiki/Atan2
	// It is then converted from radians to degrees
	#ifdef RESTRICT_PITCH // Eq. 25 and 26
	roll  = atan2(accY, accZ) * RAD_TO_DEG;
	pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
	#else // Eq. 28 and 29
	roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
	pitch = atan2(-accX, accZ) * RAD_TO_DEG;
	#endif

	double gyroXrate = gyroX / 131.0; // Convert to deg/s
	double gyroYrate = gyroY / 131.0; // Convert to deg/s

	#ifdef RESTRICT_PITCH
	// This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
	if ((roll < -90 && kalAngleX > 90) || (roll > 90 && kalAngleX < -90)) {
		setAngle(&kalmanX, roll);
		compAngleX = roll;
		kalAngleX = roll;
		gyroXangle = roll;
	} else
	kalAngleX = getAngle(&kalmanX, roll, gyroXrate, dt); // Calculate the angle using a Kalman filter

	if (abs2(kalAngleX) > 90)
	gyroYrate = -gyroYrate; // Invert rate, so it fits the restriced accelerometer reading
	kalAngleY = getAngle(&kalmanY, pitch, gyroYrate, dt);
	#else
	// This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
	if ((pitch < -90 && kalAngleY > 90) || (pitch > 90 && kalAngleY < -90)) {
		setAngle(&kalmanY, pitch);
		compAngleY = pitch;
		kalAngleY = pitch;
		gyroYangle = pitch;
	} else
	kalAngleY = getAngle(&kalmanY, pitch, gyroYrate, dt); // Calculate the angle using a Kalman filter

	if (abs2(kalAngleY) > 90)
	gyroXrate = -gyroXrate; // Invert rate, so it fits the restriced accelerometer reading
	kalAngleX = getAngle&(kalmanX, roll, gyroXrate, dt); // Calculate the angle using a Kalman filter
	#endif

	gyroXangle += gyroXrate * dt; // Calculate gyro angle without any filter
	gyroYangle += gyroYrate * dt;
	//gyroXangle += kalmanX.getRate() * dt; // Calculate gyro angle using the unbiased rate
	//gyroYangle += kalmanY.getRate() * dt;

	compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll; // Calculate the angle using a Complimentary filter
	compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch;

	// Reset the gyro angle when it has drifted too much
	if (gyroXangle < -180 || gyroXangle > 180)
	gyroXangle = kalAngleX;
	if (gyroYangle < -180 || gyroYangle > 180)
	gyroYangle = kalAngleY;
}
