// got.c
// gcc got.c -m32 -g -O0 -no-pie -Wl,-z,relro -o got
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
  char *pointer[4];
  char second[4];

  strncpy(pointer, argv[1], 4);
  printf("Ptr points to %p\n", *pointer);
  printf("Now we will copy the argv[2]: %s to the location: %p\n", argv[2], *pointer);
  strncpy(*pointer, argv[2], 4);
  printf("sh");
  return EXIT_SUCCESS;
}
