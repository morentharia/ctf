# Python program to convert a
# number from any base to decimal

# To return value of a char.
# For example, 2 is returned
# for '2'. 10 is returned for 'A',
# 11 for 'B'

# Function to convert a number
# from given base 'b' to decimal
from math import sqrt


def toDeci(str,base):
    llen = len(str)
    power = 1 #Initialize power of base
    num = 0     #Initialize result

    # Decimal equivalent is str[len-1]*1 +
    # str[len-2]*base + str[len-3]*(base^2) + ...
    for i in range(llen - 1, -1, -1):

        # A digit in input number must
        # be less than number's base
        if val(str[i]) >= base:
            print('Invalid Number')
            return -1
        num += val(str[i]) * power
        power = power * base
    return num

# Driver code
# strr = "11A"
# base = 16
# print('Decimal equivalent of', strr,
#               'in base', base, 'is',
#                  toDeci(strr, base))

# Python3 Program to convert decimal to
# any given base

# To return char for a value. For example
# '2' is returned for 2. 'A' is returned
# for 10. 'B' for 11

# Utility function to reverse a string
def strev(str):

    len = len(str);
    for i in range(int(len / 2)):
        temp = str[i];
        str[i] = str[len - i - 1];
        str[len - i - 1] = temp;

# Function to convert a given decimal
# number to a base 'base' and
def fromDeci(res, base, inputNum):

    index = 0; # Initialize index of result

    # Convert input number is given base
    # by repeatedly dividing it by base
    # and taking remainder
    while (inputNum > 0):
        res+= reVal(inputNum % base);
        inputNum = int(inputNum / base);

    # Reverse the result
    res = res[::-1];

    return res;



# # Driver Code
# inputNum = 282;
# base = 16;
# res = "";
# print("Equivalent of", inputNum, "in base",
#        base, "is", fromDeci(res, base, inputNum));

# This code is contributed by mits

# This code is contributed
# by Sahil shelangia

def val(c):
    if c >= '0' and c <= '9':
        return ord(c) - ord('0')
    if c >= 'A' and c <= 'Z':
        return ord(c) - ord('A')+10
    if c >= 'a' and c <= 'z':
        return ord(c) - ord('a')+10+26
    # else:
    #     return ord(c) - ord('A') + 10;

def reVal(num):
    if (num >= 0 and num <= 9):
        return chr(num + ord('0'));
    if (num >= 10 and num <= 10+26):
        return chr(num - 10 + ord('A'));
    else:
        return chr(num - (10+26) + ord('a'));

print('--------------')
# print(fromDeci("", 30, toDeci('A', 30)+toDeci('1', 30)))

base=62

a = toDeci('z', base)
print(a)
b = toDeci('1', base)
print(b)
res = fromDeci("", base, a + b)
# print(res)



for i in  range(1, int(sqrt(1970440568377307939233))):
    if  1970440568377307939233 % i == 0:
        b =  1970440568377307939233 /i
        print(f"{i=} {b=}")





