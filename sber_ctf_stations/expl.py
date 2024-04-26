
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
source ~/.gef-2024.01.py
set follow-fork-mode child
set detach-on-fork off

# pie b 0x26c8
# pie b 0x26cd
# pie b 0x2779
# pie b 0x2752
# pie b 0x22b9



# pie b 0x27d9
# pie b 0x281e
# pie b 0x285e

pie b 0x2835

c
# telescope $esp
# hexdump byte $rax
# ni 4
# hexdump byte $rax
'''.format(**locals())


# Set up pwntools for the correct architecture
exe = './stations'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-t", ":.1", "-p", "90"]

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
# io.sendlineafter(b':', "AAAAAAAAAA")
# io.sendlineafter(b':', "BBBBBBBBBB")
#
#--------------------
# "gEH6bGRCgl"
# "brightfutur3"
#
print(io.recvline().decode())
# io.send(b'1\n')
# io.send(b'z\n')
io.send(b'brightfutur3\n')
io.send(b'1\n')


"""
Введите коды станций для того, чтобы купить билет
Cтанция отправления: 13fz
Станция прибытия: ZkH5bYe6x
go1Ngs0uTh
"""


print(io.recvall().decode())
# io.clean()
# print(io.recvline().decode())
# io.interactive()
