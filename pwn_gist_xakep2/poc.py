import io
import json
import os
import pty
import signal
import subprocess
import sys
import threading
from multiprocessing import Process
from pprint import pp
from threading import Thread
from time import sleep

import psutil

# TARGET = './test'
TARGET = "./ovrflw"

GEF_PROMPT =  b'''gef\xe2\x9e\xa4  \x01\x1b[0m\x02]'''[:-1]

args = ["/usr/bin/gdb"]
# args += [TARGET]
gdbp = subprocess.Popen(args, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def kill_child_processes(parent_pid, sig=signal.SIGINT):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)

def ProcessTTY(master):
    line = b""
    while True:
        try:
            ch = os.read(master, 100)
        except OSError:
            # We get this exception when the spawn process closes all references to the
            # pty descriptor which we passed him to use for stdout
            # (typically when it and its childs exit)
            break
        line += ch
        print(ch.decode(), end="", flush=True)
        if 'float:' in line.decode():
            line = b""
            os.write(master, b'322 3222\n')

def readstderr():
    out=b''
    while True:
        if gdbp.poll() is not None:
            print('gdb finished')
            return ""
        ch = gdbp.stderr.read(1)
        out += ch
        if ch == b"\n":
            print(out.decode())
            out=b''


def gef(cmd=None, nowait=False):
    if gdbp.poll() is not None:
        print('gdb finished')
        return ""

    if cmd:
        if not cmd.endswith("\n"):
            cmd += "\n"
        print(cmd, end="")
        gdbp.stdin.write(cmd.encode())
        if nowait:
            return

    out=b''
    while True:
        if gdbp.poll() is not None:
            print('gdb finished')
            return ""
        out += gdbp.stdout.read(1)
        if out.endswith(GEF_PROMPT):
            print(out.decode(), end='')
            return out.decode()


stderrp = Thread(target=readstderr, args=())
stderrp.start()

master, slave = pty.openpty()
print(os.ttyname(slave))


gef()
# gef("info")
gef(f"file {TARGET}")

gef(f"tty {os.ttyname(slave)}")


tube = Process(target=ProcessTTY, args=(master,))
tube.start()



# gef("run", nowait=True)


# for i in range(1):
#     sleep(2)
#     print("hheheheheh")
#     kill_child_processes(gdbp.pid, signal.SIGINT)
#     gef()
#     gef("continue", nowait=True)

for i in range(5):
    gef("run " + i * "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    gef('x/64wx $esp-136')

tube.join()





