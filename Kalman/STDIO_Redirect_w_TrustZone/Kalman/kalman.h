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

#ifndef _KALMAN_H
#define _KALMAN_H

#include "kalman_struct.h"

//#define RESTRICT_PITCH // Comment out to restrict roll to ±90deg instead
// please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf

void initializeKalman (Kalman *kalman);

double getAngle(Kalman *kalman, double newAngle, double newRate, double dt);

void setAngle(Kalman *kalman, double newAngle);
void setQangle(Kalman *kalman, double newQ_angle);
void setQbias(Kalman *kalman, double newQ_bias);
void setRmeasure(Kalman *kalman, double newR_measure);

double getQangle(Kalman *kalman);
double getQbias(Kalman *kalman);
double getRmeasure(Kalman *kalman);

#endif
