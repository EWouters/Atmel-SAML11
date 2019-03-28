#include <stdio.h>

typedef union {
  float f;
  struct {
    unsigned int mantisa : 23;
    unsigned int exponent : 8;
    unsigned int sign : 1;
  } parts;
} float_cast;

void print_binary(unsigned int d, int size, int twos_complement, int inverse, int dot) {
  char c[256] = { '\0' };
  if (twos_complement != 0) {
        int v = ((0x01 << (size - 1)) - 1);
  	d -= v;
  }
  int i = 0;
  while (size > 0) {
      if (d & 0x01) {
	  c[i++] = '1';
      }
      else {
	  c[i++] = '0';
      }
      d >>= 1;
      size -= 1;
  }
  
  if (inverse != 0) {
          int size = i;
	  while (i > 0) {
              if (dot == (size - i)) {
		   printf(".");
              }
	      printf("%c", c[--i]);   
	  }
  }
  else {
          int j = 0;
	  while (j <= i) {
	      if (dot == (j - i)) {
		   printf(".");
	      }
	      printf("%c", c[j++]);   
	  }
  }
}

void print_float(float f) {
  float_cast d1 = { .f = f };

  float flt;

  while(1) {
   printf("Enter float: ");
   scanf("%f", &flt);
   d1.f = flt;

   int v = ((0x01 << (8 - 1)) - 1);
   int actual_exponent = d1.parts.exponent - v;

   print_binary(d1.parts.sign, 1, 0, 0, -2);
   printf(" | ");
   printf("1");
   print_binary(d1.parts.mantisa, 23, 0, 1, actual_exponent);
   //printf("1");
   printf(" | ");
   print_binary(d1.parts.exponent, 8, 1, 1, -2);
   printf(" (%u)", actual_exponent);
   //printf("1");
   printf("\n");
  }
  
  
}

int main(void) {
  //float_cast d1 = { .f = 0.9 };
  
  print_float(70.1);
  printf("\n");
  print_float(70.2);

  // 2.1    11001100110011001100000
  // 2.2    11001100110011001101
  // 2.3 10011001100110011001100000
  // 110011001100110011 % HASHSIZE=64 -> [0,64]
} 
