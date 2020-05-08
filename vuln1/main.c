#include <stdio.h>
#include <unistd.h>

int helper() {
    system("touch /pwd/vuln1/pwnd.txt");
    return 0;
}

int overflow() {
  char buffer[500];
  int userinput;
  userinput = read(0, buffer, 700);
  printf("\nUser provided %d bytes. Buffer content is: %s\n", userinput,
         buffer);
  return 0;
}

int main(int argc, char *argv[]) {
  overflow();
  /* helper(); */
  return 0;
}
