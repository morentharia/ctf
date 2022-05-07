import os
import sys

import pexpect
from pexpect import EOF, TIMEOUT
from pexpect.utils import (poll_ignore_interrupts, select_ignore_interrupts,
                           split_command_line, which)


class spawngdb(pexpect.spawn):
    def __init__(self, logo):
        super().__init__(
            "/usr/bin/gdb",
            # echo=False,
            encoding="utf-8",
            use_poll=True,
        )
        self.logo = logo
        # self.__irix_hack = None
        self.expect(self.logo)

    def read_nonblocking(self, size=1, timeout=-1):
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        if self.use_poll:

            def select(timeout):
                return poll_ignore_interrupts([self.child_fd], timeout)

        else:

            def select(timeout):
                return select_ignore_interrupts([self.child_fd], [], [], timeout)[0]

        if select(0):
            try:
                incoming = super().read_nonblocking(size)
            except EOF:
                self.isalive()
                raise
            except:
                print(f"decode error we don't care 1")
                return ""

            while len(incoming) < size and select(0):
                try:
                    incoming += super().read_nonblocking(
                        size - len(incoming)
                    )
                except EOF:
                    self.isalive()
                    return incoming
                except:
                    print("decode error we don't care 2")
                    return ""
            return incoming

        if timeout == -1:
            timeout = self.timeout

        if not self.isalive():
            if select(0):
                try:
                    return super().read_nonblocking(size)
                except:
                    print("decode error we don't care 3")
                    return ""
            self.flag_eof = True
            raise EOF("End Of File (EOF). Braindead platform.")
        # elif self.__irix_hack:
        #     if timeout is not None and timeout < 2:
        #         timeout = 2

        if (timeout != 0) and select(timeout):
            try:
                return super().read_nonblocking(size)
            except:
                print("decode error we don't care 4")
                return ""

        if not self.isalive():
            self.flag_eof = True
            raise EOF("End of File (EOF). Very slow platform.")
        else:
            raise TIMEOUT("Timeout exceeded.")

    def sendraw(self, payload):
        print(f"sendraw {payload=}")
        return os.write(self.child_fd, payload)

    def ctrl_c(self):
        self.sendcontrol("c")
        self.expect(self.logo)
        print(self.before, end="")
        print(self.logo, end="")
        sys.stdout.flush()

    def cmd(self, s):
        self.sendline(s)
        if s not in ["run", "continue"]:
            self.expect(self.logo)
            print(self.before, end="")
            print(self.logo, end="")
            sys.stdout.flush()
