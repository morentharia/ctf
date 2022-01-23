from pwn import *

TARGET = "./vuln-chat"


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
    b"""
   continue
"""
)
io.interactive()
