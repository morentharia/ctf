#!/bin/sh
while true; do
    inotifywait -e modify ./exploit.py
    clear;
    (python exploit.py; echo 'whoami; ls') | gdb -q -x script.gdb bof
done;

