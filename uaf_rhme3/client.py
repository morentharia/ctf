import socket

from pwn import log, remote


class TeamManagerClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r = None

    def connect(self):
        while True:
            try:
                self._sock.settimeout(0.5)
                self._sock.connect((self.host, self.port))
                log.info('connected!')
                break
            except:
                # log.info('.')
                continue

        self.r = remote.fromsocket(self._sock)
        self._wait_menu()


    def _wait_menu(self):
        output = self.r.recvuntil('Your choice:', timeout=2)
        log.info(output)
        return output

    def add_player(self, name):
        self.r.sendline('1')
        self.r.recvuntil('Enter player name:')
        self.r.sendline(name)
        self.r.sendline('1')
        self.r.sendline('2')
        self.r.sendline('3')
        self.r.sendline('4')
        self._wait_menu()

    def edit_player(self, name):
        # self.select_player(player_id)
        self.r.sendline('4')
        self._wait_menu()
        self.r.sendline('1')
        self.r.sendline(name)
        self._wait_menu()
        self.r.sendline('0')
        self._wait_menu()

    def select_player(self, player_id):
        self.r.sendline('3')
        self._wait_menu()
        self.r.sendline(str(player_id))
        log.info(self.r.recvrepeat(0.2))

    def show_player(self):
        self.r.sendline('5')
        output = self._wait_menu()
        return output

    def remove_player(self, player_id):
        self.r.sendline('2')
        self.r.sendline(str(player_id))
        self._wait_menu()

    def print_team(self):
        self.r.sendline('6')
        log.info(self.r.recvrepeat(0.2))
        self._wait_menu()

    def close(self):
        self._sock.close()


    def interactive(self):
        self.r.interactive()
