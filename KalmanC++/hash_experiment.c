#include <stdio.h>

typedef union {
  float f;
  struct {
    unsigned int mantisa : 23;
    unsigned int exponent : 8;
    unsigned int sign : 1;
  } parts;
} float_cast;

void print_binary(unsigned int d) {
  char c[256] = { '\0' };
  int i = 0;
  while (d > 0) {
      if (d & 0x01) {
          c[i++] = '1';
      }
      else {
          c[i++] = '0';
      }
      d >>= 1;
  }
  
  while (i >= 0) {
      printf("%c", c[--i]);   
  }
}

void print_float(float f, int move) {
  float_cast d1 = { .f = f };
  
  printf("sign = ");
  print_binary(d1.parts.sign);
  printf("\n");
  
  printf("sign = ");
  printf("%u", d1.parts.sign);
  printf("\n");  
  
  printf("exponent = ");
  print_binary(d1.parts.exponent);
  printf("\n");
  
  printf("exponent = ");
  printf("%u", d1.parts.exponent);
  printf("\n");  
  
  printf("mantisa = ");
  print_binary(d1.parts.mantisa);
  printf("\n");
  
  printf("mantisa = ");
  printf("%u", d1.parts.mantisa >> move);
  printf("\n");  
}

int main(void) {
  //float_cast d1 = { .f = 0.9 };
  
  print_float(1.4, 2);
  printf("\n");
  print_float(1.1, 0);
  
  
  print_binary(10);
} 
