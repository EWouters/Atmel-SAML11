/* Copyright (C) 2012 Kristian Lauszus, TKJ Electronics. All rights reserved.

 This software may be distributed and modified under the terms of the GNU
 General Public License version 2 (GPL2) as published by the Free Software
 Foundation and appearing in the file GPL2.TXT included in the packaging of
 this file. Please note that GPL2 Section 2[b] requires that all works based
 on this software must also be made publicly available under the terms of
 the GPL2 ("Copyleft").

 Contact information
 -------------------

 Kristian Lauszus, TKJ Electronics
 Web      :  http://www.tkjelectronics.com
 e-mail   :  kristianl@tkjelectronics.com
 */

#include <fstream>
#include <cstring>
#include <cstdlib>
#include <cmath>
#include "kalman.h" // Source: https://github.com/TKJElectronics/KalmanFilter

#define RAD_TO_DEG 57.295779513082321

#define RESTRICT_PITCH // Comment out to restrict roll to ±90deg instead 
		       // please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf

Kalman kalmanX; // Create the Kalman instances
Kalman kalmanY;

double accX, accY, accZ;
double gyroX, gyroY, gyroZ;

double gyroXangle, gyroYangle; // Angle calculate using the gyro only
double compAngleX, compAngleY; // Calculated angle using a complementary filter
double kalAngleX, kalAngleY; // Calculated angle using a Kalman filter

static void readline(char * line, FILE * fp) {
    fgets(line, 1000, fp);
}

static void skipline(FILE * fp) {
    char line[1000];
    readline(line, fp);
}

static void readAcc(FILE * fp) {
    char line[1000];

    readline(line, fp);

    char * p = strtok(line, ",");
    
    p = strtok(NULL, ","); // skip first number

    accX = atof(p);
    p = strtok(NULL, ",");

    accY = atof(p);
    p = strtok(NULL, ",");

    accZ = atof(p);
    p = strtok(NULL, ",");
}

static void readGyro(FILE * fp) {
    char line[1000];

    readline(line, fp);

    char * p = strtok(line, ",");
    
    p = strtok(NULL, ","); // skip first number

    gyroX = atof(p);
    p = strtok(NULL, ",");

    gyroY = atof(p);
    p = strtok(NULL, ",");

    gyroZ = atof(p);
    p = strtok(NULL, ",");
}

void printDouble(double dbl, int accuracy) {
	int dblSign = (dbl < 0) ? -1 : 1;
	dbl = (dbl < 0) ? -dbl : dbl;
	
	unsigned long int tmpInt = dbl; // Get the integer side
	
	if (dblSign < 0) {
		printf("-%lu.", tmpInt); // Print sign and integer
	}
	else {
		printf("%lu.", tmpInt); // Print sign and integer
	}
	
	int i;
	for (i=0; i<accuracy; i++) {
		dbl = dbl - tmpInt; // Get the fraction
		tmpInt = dbl * 1000000; // Turn fraction to integer
		dbl  = dbl * 1000000;
		
		printf("%06lu", tmpInt); // Print fraction
	}
}

void printValuesExtended(int idx, double roll, double pitch, double gyroXangle, double gyroYangle, double compAngleX, double compAngleY, double kalAngleX, double kalAngleY) {
	printf("%d,", idx);
	printDouble(roll, 1);
	printf(",");
	printDouble(pitch, 1);
	printf(",");
	printDouble(gyroXangle, 1);
	printf(",");
	printDouble(gyroYangle, 1);
	printf(",");
	printDouble(compAngleX, 1);
	printf(",");
	printDouble(compAngleY, 1);
	printf(",");
	printDouble(kalAngleX, 1);
	printf(",");
	printDouble(kalAngleY, 1);
	printf("\n");
}

void loop(int idx, FILE *accFile, FILE *gyroFile) {
  /* Update all the values */
  readAcc(accFile);
  readGyro(gyroFile);

  double dt = 1; // Calculate delta time

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees
#ifdef RESTRICT_PITCH // Eq. 25 and 26
  double roll  = atan2(accY, accZ) * RAD_TO_DEG;
  double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
#else // Eq. 28 and 29
  double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
  double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
#endif

  double gyroXrate = gyroX / 131.0; // Convert to deg/s
  double gyroYrate = gyroY / 131.0; // Convert to deg/s

#ifdef RESTRICT_PITCH
  // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
  if ((roll < -90 && kalAngleX > 90) || (roll > 90 && kalAngleX < -90)) {
    kalmanX.setAngle(roll);
    compAngleX = roll;
    kalAngleX = roll;
    gyroXangle = roll;
  } else
    kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt); // Calculate the angle using a Kalman filter

  if (abs(kalAngleX) > 90)
    gyroYrate = -gyroYrate; // Invert rate, so it fits the restriced accelerometer reading
  kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt);
#else
  // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
  if ((pitch < -90 && kalAngleY > 90) || (pitch > 90 && kalAngleY < -90)) {
    kalmanY.setAngle(pitch);
    compAngleY = pitch;
    kalAngleY = pitch;
    gyroYangle = pitch;
  } else
    kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt); // Calculate the angle using a Kalman filter

  if (abs(kalAngleY) > 90)
    gyroXrate = -gyroXrate; // Invert rate, so it fits the restriced accelerometer reading
  kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt); // Calculate the angle using a Kalman filter
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

  /* Print Data */
  //fprintf(output, "%d,%f,%f,%f,%f,%f,%f,%f,%f\r\n", idx+1, roll, pitch, gyroXangle, gyroYangle, compAngleX, compAngleY, kalAngleX, kalAngleY);
  printValuesExtended(idx+2, roll, pitch, gyroXangle, gyroYangle, compAngleX, compAngleY, kalAngleX, kalAngleY);
}

int main() {

  // Open input data file
  FILE *accFile = fopen("input_acc.csv", "r");
  FILE *gyroFile = fopen("input_gyro.csv", "r");
  //FILE *output = fopen("output.csv", "w");

  // Skip CSV header
  skipline(accFile);
  skipline(gyroFile);

  /* Set kalman and gyro starting angle */
  readAcc(accFile);
  readGyro(gyroFile);

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees
#ifdef RESTRICT_PITCH // Eq. 25 and 26
  double roll  = atan2(accY, accZ) * RAD_TO_DEG;
  double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
#else // Eq. 28 and 29
  double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
  double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
#endif

  kalmanX.setAngle(roll); // Set starting angle
  kalmanY.setAngle(pitch);
  gyroXangle = roll;
  gyroYangle = pitch;
  compAngleX = roll;
  compAngleY = pitch;

  //fprintf(output, ",Roll,Pitch,GyroX,CompX,KalmanX,GyroY,CompY,KalmanY\r\n");
  printValuesExtended(1, roll, pitch, gyroXangle, gyroYangle, compAngleX, compAngleY, kalAngleX, kalAngleY);

  int i;
  for (i = 0; i < 1001; i++) loop(i, accFile, gyroFile);

  fclose(accFile);
  fclose(gyroFile);
  //fclose(output);

  return 0;
}


