#include <atmel_start.h>
#include "quicksort.h"

/*
These values have been generated using the following python script:

import numpy as np
np.random.seed(314)
n = 256
int_max = 255
randints = np.random.randint(int_max, size=n)
print(list(randints))
randints.sort()
print(list(randints))

*/

// Tests show that the max stack pointer for this algorithm is 1544 + N (or 0x608 + N in hex). With or without GPIO initialization.
// Tests show that the max stack pointer for this algorithm is 1680 + N (or 0x690 + N in hex). With STDIO redirect enabled.

#define N 256 // 1024

#if(N == 256)
uint8_t values[N] = { 8, 109, 201, 179, 86, 42, 206, 240, 7, 226, 186, 120, 86, 71, 80, 163, 108, 150, 7, 88, 4, 160, 91, 68, 173, 104, 88, 144, 111, 9, 61, 54, 45, 66, 71, 86, 227, 123, 164, 136, 50, 0, 135, 227, 82, 57, 88, 165, 205, 189, 246, 221, 63, 91, 107, 9, 213, 132, 178, 137, 110, 86, 139, 18, 16, 85, 102, 124, 111, 242, 128, 208, 186, 97, 22, 250, 154, 222, 65, 222, 194, 187, 241, 189, 233, 44, 112, 66, 177, 135, 145, 3, 208, 100, 91, 187, 231, 165, 3, 239, 42, 165, 188, 208, 67, 42, 144, 110, 31, 211, 225, 225, 38, 85, 85, 203, 27, 200, 176, 48, 1, 153, 20, 52, 86, 101, 39, 211, 213, 233, 190, 60, 121, 69, 238, 250, 190, 89, 99, 180, 245, 33, 83, 157, 135, 235, 216, 206, 249, 178, 55, 208, 179, 141, 155, 33, 111, 254, 63, 39, 134, 95, 244, 182, 68, 71, 220, 134, 227, 74, 5, 230, 74, 158, 109, 46, 77, 27, 90, 18, 15, 158, 93, 8, 135, 150, 10, 86, 134, 191, 62, 32, 23, 167, 142, 141, 247, 57, 106, 195, 75, 238, 187, 112, 182, 38, 62, 103, 44, 252, 48, 38, 219, 87, 243, 46, 135, 232, 186, 11, 146, 96, 222, 32, 161, 32, 27, 183, 86, 223, 107, 207, 10, 195, 45, 196, 72, 161, 186, 127, 26, 17, 244, 170, 210, 49, 111, 68, 32, 140, 94, 222, 161, 98, 180, 34 };
#elif(N == 1024)
uint8_t values[N] = { 8, 109, 201, 179, 86, 42, 206, 240, 7, 226, 186, 120, 86, 71, 80, 163, 108, 150, 7, 88, 4, 160, 91, 68, 173, 104, 88, 144, 111, 9, 61, 54, 45, 66, 71, 86, 227, 123, 164, 136, 50, 0, 135, 227, 82, 57, 88, 165, 205, 189, 246, 221, 63, 91, 107, 9, 213, 132, 178, 137, 110, 86, 139, 18, 16, 85, 102, 124, 111, 242, 128, 208, 186, 97, 22, 250, 154, 222, 65, 222, 194, 187, 241, 189, 233, 44, 112, 66, 177, 135, 145, 3, 208, 100, 91, 187, 231, 165, 3, 239, 42, 165, 188, 208, 67, 42, 144, 110, 31, 211, 225, 225, 38, 85, 85, 203, 27, 200, 176, 48, 1, 153, 20, 52, 86, 101, 39, 211, 213, 233, 190, 60, 121, 69, 238, 250, 190, 89, 99, 180, 245, 33, 83, 157, 135, 235, 216, 206, 249, 178, 55, 208, 179, 141, 155, 33, 111, 254, 63, 39, 134, 95, 244, 182, 68, 71, 220, 134, 227, 74, 5, 230, 74, 158, 109, 46, 77, 27, 90, 18, 15, 158, 93, 8, 135, 150, 10, 86, 134, 191, 62, 32, 23, 167, 142, 141, 247, 57, 106, 195, 75, 238, 187, 112, 182, 38, 62, 103, 44, 252, 48, 38, 219, 87, 243, 46, 135, 232, 186, 11, 146, 96, 222, 32, 161, 32, 27, 183, 86, 223, 107, 207, 10, 195, 45, 196, 72, 161, 186, 127, 26, 17, 244, 170, 210, 49, 111, 68, 32, 140, 94, 222, 161, 98, 180, 34, 121, 124, 45, 86, 13, 184, 197, 169, 92, 108, 139, 92, 165, 44, 180, 196, 19, 142, 146, 228, 110, 181, 111, 100, 39, 227, 149, 123, 23, 44, 193, 92, 237, 126, 127, 30, 104, 60, 83, 98, 113, 71, 88, 143, 183, 230, 5, 0, 212, 148, 123, 154, 132, 60, 240, 25, 42, 5, 248, 247, 43, 84, 174, 186, 9, 155, 129, 245, 231, 114, 4, 213, 246, 170, 115, 114, 101, 212, 245, 223, 89, 126, 39, 255, 167, 61, 240, 186, 177, 148, 54, 215, 104, 36, 141, 232, 115, 79, 219, 211, 85, 221, 160, 29, 38, 184, 254, 3, 143, 78, 212, 83, 38, 81, 176, 200, 110, 138, 17, 120, 98, 101, 44, 179, 184, 135, 162, 34, 6, 15, 76, 167, 153, 247, 208, 61, 253, 5, 41, 153, 175, 133, 26, 58, 229, 78, 253, 28, 244, 141, 25, 197, 178, 62, 80, 73, 1, 149, 75, 221, 126, 36, 68, 72, 182, 184, 154, 68, 133, 242, 208, 0, 0, 16, 201, 71, 26, 64, 188, 245, 214, 14, 158, 83, 228, 117, 118, 120, 168, 74, 46, 50, 190, 131, 51, 51, 107, 39, 109, 143, 53, 253, 29, 106, 108, 62, 122, 150, 248, 198, 119, 160, 70, 119, 72, 96, 84, 62, 90, 230, 51, 109, 107, 218, 156, 171, 59, 25, 127, 201, 86, 204, 191, 190, 77, 56, 77, 104, 250, 145, 65, 182, 165, 52, 222, 175, 192, 209, 44, 174, 43, 154, 125, 109, 203, 169, 202, 32, 118, 175, 184, 244, 135, 148, 24, 234, 112, 82, 237, 158, 167, 144, 6, 93, 24, 208, 207, 99, 100, 87, 141, 181, 102, 61, 201, 230, 83, 42, 170, 159, 48, 184, 7, 135, 109, 213, 248, 184, 71, 62, 78, 204, 225, 107, 21, 68, 28, 22, 228, 16, 14, 105, 216, 153, 162, 122, 39, 208, 157, 236, 44, 218, 7, 236, 221, 66, 208, 103, 81, 10, 167, 16, 209, 37, 83, 197, 195, 135, 210, 209, 5, 233, 98, 199, 55, 147, 76, 43, 47, 3, 112, 179, 36, 48, 87, 180, 200, 165, 171, 206, 199, 73, 46, 114, 41, 38, 243, 219, 53, 194, 89, 76, 74, 40, 64, 13, 101, 36, 194, 27, 82, 161, 179, 224, 223, 241, 47, 146, 219, 247, 203, 21, 99, 82, 187, 122, 130, 67, 130, 155, 130, 22, 31, 125, 115, 245, 84, 99, 250, 112, 75, 67, 128, 7, 164, 246, 177, 101, 6, 135, 212, 218, 13, 34, 84, 76, 41, 195, 98, 249, 214, 192, 248, 89, 214, 208, 74, 192, 182, 143, 255, 44, 84, 159, 253, 78, 24, 76, 251, 213, 41, 18, 234, 94, 66, 213, 210, 44, 113, 69, 193, 149, 49, 8, 63, 0, 179, 211, 228, 129, 149, 17, 11, 241, 209, 112, 22, 243, 172, 174, 111, 42, 147, 94, 153, 164, 56, 19, 212, 49, 157, 253, 47, 103, 234, 184, 170, 166, 214, 93, 47, 10, 32, 132, 154, 166, 188, 90, 56, 17, 72, 184, 41, 2, 241, 87, 156, 194, 7, 36, 185, 207, 188, 242, 183, 141, 178, 64, 68, 85, 2, 215, 65, 155, 104, 5, 192, 176, 43, 219, 24, 103, 250, 247, 70, 81, 86, 10, 71, 14, 168, 156, 77, 92, 74, 175, 236, 136, 215, 1, 40, 166, 116, 187, 74, 242, 99, 103, 123, 142, 109, 146, 247, 32, 126, 244, 237, 39, 31, 54, 95, 87, 54, 23, 89, 177, 62, 34, 29, 192, 136, 160, 53, 29, 254, 34, 159, 162, 112, 215, 12, 172, 181, 143, 161, 73, 171, 235, 83, 118, 105, 9, 103, 55, 29, 229, 68, 135, 167, 191, 195, 166, 214, 47, 225, 122, 17, 84, 122, 131, 84, 111, 83, 246, 143, 144, 15, 224, 64, 14, 160, 137, 175, 140, 219, 105, 13, 247, 253, 175, 143, 128, 126, 52, 252, 23, 32, 166, 9, 161, 147, 77, 184, 123, 111, 111, 138, 190, 165, 109, 23, 203, 181, 220, 126, 3, 145, 231, 62, 26, 22, 167, 31, 198, 112, 56, 62, 25, 186, 161, 53, 91, 255, 54, 56, 36, 79, 183, 254, 227, 9, 145, 69, 31, 84, 252, 53, 5, 146, 101, 76, 25, 102, 230, 137, 162, 97, 239, 38, 81, 158, 71, 224, 73, 172, 31, 244, 212, 193, 137, 37, 188, 186, 188, 187, 213, 90, 246, 98, 175, 117, 18, 95, 19, 144, 14, 124, 144, 14, 102, 156, 1, 251, 157, 242, 109, 80, 98, 92, 230, 206, 135, 138, 153, 218, 151, 91, 165 };
#else
#error Only 256 and 1024 are supported for N
#endif

//#define CHECK_RESULT
#ifdef CHECK_RESULT
#if(N == 256)
const uint8_t sorted[N] = { 0, 1, 3, 3, 4, 5, 7, 7, 8, 8, 9, 9, 10, 10, 11, 15, 16, 17, 18, 18, 20, 22, 23, 26, 27, 27, 27, 31, 32, 32, 32, 32, 33, 33, 34, 38, 38, 38, 39, 39, 42, 42, 42, 44, 44, 45, 45, 46, 46, 48, 48, 49, 50, 52, 54, 55, 57, 57, 60, 61, 62, 62, 63, 63, 65, 66, 66, 67, 68, 68, 68, 69, 71, 71, 71, 72, 74, 74, 75, 77, 80, 82, 83, 85, 85, 85, 86, 86, 86, 86, 86, 86, 86, 87, 88, 88, 88, 89, 90, 91, 91, 91, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 106, 107, 107, 108, 109, 109, 110, 110, 111, 111, 111, 111, 112, 112, 120, 121, 123, 124, 127, 128, 132, 134, 134, 134, 135, 135, 135, 135, 135, 136, 137, 139, 140, 141, 141, 142, 144, 144, 145, 146, 150, 150, 153, 154, 155, 157, 158, 158, 160, 161, 161, 161, 163, 164, 165, 165, 165, 167, 170, 173, 176, 177, 178, 178, 179, 179, 180, 180, 182, 182, 183, 186, 186, 186, 186, 187, 187, 187, 188, 189, 189, 190, 190, 191, 194, 195, 195, 196, 200, 201, 203, 205, 206, 206, 207, 208, 208, 208, 208, 210, 211, 211, 213, 213, 216, 219, 220, 221, 222, 222, 222, 222, 223, 225, 225, 226, 227, 227, 227, 230, 231, 232, 233, 233, 235, 238, 238, 239, 240, 241, 242, 243, 244, 244, 245, 246, 247, 249, 250, 250, 252, 254 };
#elif(N == 1024)
const uint8_t sorted[N] = { 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 12, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 17, 18, 18, 18, 18, 19, 19, 19, 20, 21, 21, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 24, 24, 24, 24, 25, 25, 25, 25, 25, 26, 26, 26, 26, 27, 27, 27, 27, 28, 28, 29, 29, 29, 29, 29, 30, 31, 31, 31, 31, 31, 31, 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 34, 34, 34, 34, 34, 36, 36, 36, 36, 36, 36, 37, 37, 38, 38, 38, 38, 38, 38, 38, 39, 39, 39, 39, 39, 39, 39, 40, 40, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 42, 43, 43, 43, 43, 44, 44, 44, 44, 44, 44, 44, 44, 44, 45, 45, 45, 46, 46, 46, 46, 47, 47, 47, 47, 47, 48, 48, 48, 48, 49, 49, 49, 50, 50, 51, 51, 51, 52, 52, 52, 53, 53, 53, 53, 53, 54, 54, 54, 54, 54, 55, 55, 55, 56, 56, 56, 56, 56, 57, 57, 58, 59, 60, 60, 60, 61, 61, 61, 61, 62, 62, 62, 62, 62, 62, 62, 62, 62, 63, 63, 63, 64, 64, 64, 64, 65, 65, 65, 66, 66, 66, 66, 67, 67, 67, 68, 68, 68, 68, 68, 68, 68, 68, 69, 69, 69, 70, 70, 71, 71, 71, 71, 71, 71, 71, 71, 72, 72, 72, 72, 73, 73, 73, 73, 74, 74, 74, 74, 74, 74, 74, 75, 75, 75, 76, 76, 76, 76, 76, 76, 77, 77, 77, 77, 77, 78, 78, 78, 78, 79, 79, 80, 80, 80, 81, 81, 81, 81, 82, 82, 82, 82, 83, 83, 83, 83, 83, 83, 83, 83, 84, 84, 84, 84, 84, 84, 84, 84, 85, 85, 85, 85, 85, 86, 86, 86, 86, 86, 86, 86, 86, 86, 86, 87, 87, 87, 87, 87, 88, 88, 88, 88, 89, 89, 89, 89, 89, 90, 90, 90, 90, 91, 91, 91, 91, 91, 92, 92, 92, 92, 92, 93, 93, 93, 94, 94, 94, 95, 95, 95, 96, 96, 97, 97, 98, 98, 98, 98, 98, 98, 98, 99, 99, 99, 99, 99, 100, 100, 100, 101, 101, 101, 101, 101, 101, 102, 102, 102, 102, 103, 103, 103, 103, 103, 103, 104, 104, 104, 104, 104, 105, 105, 105, 106, 106, 107, 107, 107, 107, 107, 108, 108, 108, 109, 109, 109, 109, 109, 109, 109, 109, 109, 110, 110, 110, 110, 111, 111, 111, 111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112, 113, 113, 114, 114, 114, 115, 115, 115, 116, 117, 117, 118, 118, 118, 119, 119, 120, 120, 120, 121, 121, 122, 122, 122, 122, 122, 123, 123, 123, 123, 123, 124, 124, 124, 125, 125, 126, 126, 126, 126, 126, 126, 127, 127, 127, 128, 128, 128, 129, 129, 130, 130, 130, 131, 131, 132, 132, 132, 133, 133, 134, 134, 134, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 136, 136, 136, 137, 137, 137, 137, 138, 138, 138, 139, 139, 140, 140, 141, 141, 141, 141, 141, 141, 142, 142, 142, 143, 143, 143, 143, 143, 143, 143, 144, 144, 144, 144, 144, 144, 145, 145, 145, 145, 146, 146, 146, 146, 146, 147, 147, 147, 148, 148, 148, 149, 149, 149, 149, 150, 150, 150, 151, 153, 153, 153, 153, 153, 153, 154, 154, 154, 154, 154, 155, 155, 155, 155, 156, 156, 156, 156, 157, 157, 157, 157, 158, 158, 158, 158, 158, 159, 159, 159, 160, 160, 160, 160, 160, 161, 161, 161, 161, 161, 161, 161, 162, 162, 162, 162, 163, 164, 164, 164, 165, 165, 165, 165, 165, 165, 165, 165, 166, 166, 166, 166, 166, 167, 167, 167, 167, 167, 167, 167, 168, 168, 169, 169, 170, 170, 170, 170, 171, 171, 171, 172, 172, 172, 173, 174, 174, 174, 175, 175, 175, 175, 175, 175, 175, 176, 176, 176, 177, 177, 177, 177, 178, 178, 178, 178, 179, 179, 179, 179, 179, 179, 180, 180, 180, 180, 181, 181, 181, 181, 182, 182, 182, 182, 182, 183, 183, 183, 183, 184, 184, 184, 184, 184, 184, 184, 184, 184, 184, 185, 186, 186, 186, 186, 186, 186, 186, 186, 187, 187, 187, 187, 187, 187, 188, 188, 188, 188, 188, 188, 189, 189, 190, 190, 190, 190, 190, 191, 191, 191, 192, 192, 192, 192, 192, 193, 193, 193, 194, 194, 194, 194, 195, 195, 195, 195, 195, 196, 196, 197, 197, 197, 198, 198, 199, 199, 200, 200, 200, 201, 201, 201, 201, 202, 203, 203, 203, 203, 204, 204, 205, 206, 206, 206, 206, 207, 207, 207, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 209, 209, 209, 209, 210, 210, 210, 211, 211, 211, 211, 212, 212, 212, 212, 212, 212, 213, 213, 213, 213, 213, 213, 213, 214, 214, 214, 214, 214, 215, 215, 215, 215, 216, 216, 218, 218, 218, 218, 219, 219, 219, 219, 219, 219, 220, 220, 221, 221, 221, 221, 222, 222, 222, 222, 222, 223, 223, 223, 224, 224, 224, 225, 225, 225, 225, 226, 227, 227, 227, 227, 227, 228, 228, 228, 228, 229, 229, 230, 230, 230, 230, 230, 230, 231, 231, 231, 232, 232, 233, 233, 233, 234, 234, 234, 235, 235, 236, 236, 236, 237, 237, 237, 238, 238, 239, 239, 240, 240, 240, 241, 241, 241, 241, 242, 242, 242, 242, 242, 243, 243, 243, 244, 244, 244, 244, 244, 244, 245, 245, 245, 245, 245, 246, 246, 246, 246, 246, 247, 247, 247, 247, 247, 247, 247, 248, 248, 248, 248, 249, 249, 250, 250, 250, 250, 250, 251, 251, 252, 252, 252, 253, 253, 253, 253, 253, 253, 254, 254, 254, 254, 255, 255, 255 };
#endif
#endif

#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	START_MEASURE(DGI_GPIO2);
	quicksort(values, 0, N-1);
	STOP_MEASURE(DGI_GPIO2);

#ifdef CHECK_RESULT
	for (size_t i = 0; i < N; i++) {
		if (values[i] != sorted[i]) {
			while(1) {}
		}
	}
#endif

	END_MEASUREMENT;
	
	return 0;
}