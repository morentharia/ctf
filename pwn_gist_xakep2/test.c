#include <stdio.h>
int main()
{
    int a;
    float b;

    printf("Enter integer and then a float: ");
  
    // Taking multiple inputs
    scanf("%d%f", &a, &b);

    printf("You entered %d and %f\n", a, b);  

    printf("Enter integer and then a float AGAin: ");
    scanf("%d%f", &a, &b);
    printf("You entered AGAIN %d and %f\n", a, b);  
    return 0;
}
