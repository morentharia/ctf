import termios, fcntl, sys, os

def getch():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                return c
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


if __name__ == "__main__":
    snapshot_num = 1

    while True:
        filename = 'snapshot_%03d' % snapshot_num
        os.system("clear")
        print(filename)
        os.system("cat %s" % filename)

        c = getch()
        print(c)
        if c == 'l':
            snapshot_num += 1
        elif c == 'h':
            snapshot_num -= 1
