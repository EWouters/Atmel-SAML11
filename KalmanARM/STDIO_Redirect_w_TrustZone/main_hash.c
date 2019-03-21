﻿//#include <atmel_start.h>
//
//#include "stdio_start.h"
//#include "PrintLines/printlines.h"
//
//#include "Kalman/kalman.h"
//#include "Kalman/kalman_main.h"
//#include "Kalman/kalman_globals.h"
//
//#include "HashTable/hashtable.h"
//
//#include "globals.h"
//
//#include "Measurements/measurements.h"
//#include <hal_gpio.h>
//
//#include <tgmath.h>
//
//extern HASHTABLE_ITER_TYPE selectedIter;
//extern struct hentry hashtab[HASHSIZE];
//
//int main(void)
//{
	////char line[LINE_LENGTH] = {'\0'};
	////char buffer[LINE_LENGTH] = {'\0'};
	//
	//usart_sync_get_io_descriptor(&TARGET_IO, &io);
//
	///* Initializes MCU, drivers and middleware */
	//atmel_start_init();
//
	//DONT_MEASURE();
	//
	//printf("RDY\r\n");
	//
	//readValues(&accX, &accY, &accZ);
	//readValues(&gyroX, &gyroY, &gyroZ);
	//
	//MEASURE();
//
	//// Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
	//// atan2 outputs the value of -? to ? (radians) - see http://en.wikipedia.org/wiki/Atan2
	//// It is then converted from radians to degrees
	//#ifdef RESTRICT_PITCH // Eq. 25 and 26
	//double roll  = atan2(accY, accZ) * RAD_TO_DEG;
	//double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
	//#else // Eq. 28 and 29
	//double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
	//double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
	//#endif
	//
	//initializeKalman(&kalmanX);
	//initializeKalman(&kalmanY);
//
	//setAngle(&kalmanX, roll); // Set starting angle
	//setAngle(&kalmanY, pitch);
	//gyroXangle = roll;
	//gyroYangle = pitch;
	//compAngleX = roll;
	//compAngleY = pitch;
	//
	//DONT_MEASURE();
//
	//printValuesExtended(1, roll, pitch, gyroXangle, gyroYangle, compAngleX, compAngleY, kalAngleX, kalAngleY);
	//
	//MEASURE();
//
	//int i;
	//for (i = 0; i < 1000; i++) {
		//
		//DONT_MEASURE();
		//
		///* Update all the values */
		//readValues(&accX, &accY, &accZ);
		//readValues(&gyroX, &gyroY, &gyroZ);
		//
		//MEASURE();
		//
		//selectedIter = NOT_FOUND;
		//lookup();
		//
		//if (selectedIter == NOT_FOUND) {
			//loop(i);
			//
			//hash();
			//store();
		//}
		//else {
			//MEASURE(); 
			//
			//roll = selectedIter->roll;
			//pitch = selectedIter->pitch;
			//gyroXangle = selectedIter->gyroXangle;
			//gyroYangle = selectedIter->gyroYangle;
			//compAngleX = selectedIter->compAngleX;
			//compAngleY = selectedIter->compAngleY;
			//kalAngleX = selectedIter->kalAngleX;
			//kalAngleY = selectedIter->kalAngleY;
		//}
		//
		//DONT_MEASURE();
		//
		//printValuesExtended(i, roll, pitch, gyroXangle, gyroYangle, compAngleX, compAngleY, kalAngleX, kalAngleY);
		//
		//MEASURE();
		//
	//}
	//
	///* Replace with your application code */
	//while (1) {
		//1+1;
	//}
//}