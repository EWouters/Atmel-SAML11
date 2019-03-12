clear all;
close all;

length=1000;
input_acc = csvread('input_acc.csv',1,0);
input_gyro = csvread('input_gyro.csv',1,0);
time_acc = input_acc(1:length, 1) + 1;
time_gyro = input_gyro(1:length, 1) + 1;
accX = input_acc(1:length, 2);
accY = input_acc(1:length, 3);
accZ = input_acc(1:length, 4);
gyroX_ = input_gyro(1:length, 2);
gyroY_ = input_gyro(1:length, 3);
gyroZ_ = input_gyro(1:length, 4);

output_array = csvread('output.csv',1,0);
time = output_array(1:length, 1);
roll = output_array(1:length, 2);
pitch = output_array(1:length, 3);
gyroX = output_array(1:length, 4);
compX = output_array(1:length, 5);
kalX = output_array(1:length, 6);
gyroY = output_array(1:length, 7);
compY = output_array(1:length, 8);
kalY = output_array(1:length, 9);

subplot(5,3,1);
plot(time,roll,"r-",time,compY,'b-')
title("Roll (red) + CompY (blue)");
subplot(5,3,2);
plot(time,pitch,"r-",time,kalY,"b-");
title("Pitch (red) + KalY (blue)");
subplot(5,3,3);
plot(time,gyroX,"r-",time,gyroY,"b-")
title("GyroX (red) + GyroY (blue)");
subplot(5,3,4);
plot(time,compX,"r-",time,compY,"b-");
title("CompX (red) + CompY (blue)");
subplot(5,3,5);
plot(time,kalX,"r-",time,kalY,"b-");
title("KalX (red) + KalY (blue)9");
subplot(5,3,7);
plot(time_acc,accX,"r-");
title("AccX");
subplot(5,3,8);
plot(time_acc,accY,"r-");
title("AccY");
subplot(5,3,9);
plot(time_acc,accZ,"r-");
title("AccZ");
subplot(5,3,10);
plot(time_gyro,gyroX_,"b-");
title("GyroX");
subplot(5,3,11);
plot(time_gyro,gyroY_,"b-");
title("GyroY");
subplot(5,3,12);
plot(time_gyro,gyroZ_,"b-");
title("GyroZ");


