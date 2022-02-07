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

GEF_PROMPT =  b'''gef\xe2\x9e\xa4  \x01\x1b[0m\x02]'''[:-1]

def kill_child_processes(parent_pid, sig=signal.SIGINT):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)

def processio(ifunc):
    master, slave = pty.openpty()
    print(os.ttyname(slave))


    def ProcessTTY(master, ifunc):
        buf = b""

        def write(data):
            # clean_buf()
            # print(" >>> "+ data, end="")
            os.write(master, data)

        # def clean_buf():
        #     nonlocal buf
        #     line = b""

        zzz = ifunc(write)
        next(zzz)


        while True:
            ch = os.read(master, 1000)
            # try:
            #     ch = os.read(master, 1000)
            # except OSError:
            #     # We get this exception when the spawn process closes all references to the
            #     # pty descriptor which we passed him to use for stdout
            #     # (typically when it and its childs exit)
            #     break

            buf += ch
            print(buf)
            lol = zzz.send(buf)
            if lol:
                print("input> ", lol)
                write(lol)
                ch = os.read(master, len(lol))
                buf = b""

    tube = Thread(target=ProcessTTY, args=(master, ifunc))
    tube.start()
    return tube.join, os.ttyname(slave)


def opengdb():
    args = ["/usr/bin/gdb"]
    # args += [TARGET]
    gdbp = subprocess.Popen(args, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

    stderrp = Thread(target=readstderr, args=())
    stderrp.start()

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
                print(out.decode(), end='', flush=True)
                return out.decode()

    def ctrl_c():
        kill_child_processes(gdbp.pid, signal.SIGINT)


    return gef, ctrl_c
