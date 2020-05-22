#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
  // 128-байтный массив типа char
  char buf[128];
  // копирование первого аргумента в массив buf
  strcpy(buf, argv[1]);
  // вывод содержимого буфера на экран
  printf("Input: %s\n", buf);
  return 0;
}
