import sys
from pprint import pp
from time import sleep

import pexpect

LOGO = 'gef➤'

# from pexpect import replwrap

TARGET = './test'
# TARGET = "./ovrflw"
class Log():
    def write(self, data):
        try:
            data = data.decode()
        except:
            pass
        sys.stdout.write(data)
        sys.stdout.flush()
    def flush(self):
        sys.stdout.flush()


gdb = pexpect.spawn(
    '/usr/bin/gdb',
    echo=False,
    encoding='utf-8',
    logfile=Log(),
)
gdb.expect(LOGO)

def cmd(s):
    if s=='ctrl_c':
        gdb.sendcontrol('c')
        gdb.expect(LOGO)

    gdb.sendline(s)
    if s not in ['run', 'continue']:
        gdb.expect(LOGO)


cmd(f"file {TARGET}")
cmd(f"run")

gdb.expect("float:")
gdb.sendline("3 3")
gdb.expect("You entered")

cmd('ctrl_c')
cmd('x/64wx $rsp')
cmd('bt')
cmd("continue")

gdb.sendline("9 9")

gdb.expect(LOGO)
sys.stdout.flush()
