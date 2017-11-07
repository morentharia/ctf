import socket

from pwn import log, remote


class TeamManagerClient(object):
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__r = None

    def connect(self):
        while True:
            try:
                self.__sock.settimeout(0.5)
                self.__sock.connect((self.__host, self.__port))
                log.info('connected!')
                break
            except:
                # log.info('.')
                continue

        self.__r = remote.fromsocket(self.__sock)
        self._wait_menu()

    def __getattr__(self, name):
        return getattr(self.__r, name)

    def _wait_menu(self):
        output = self.recvuntil('Your choice:', timeout=2)
        log.info(output)
        return output

    def add_player(self, name):
        self.sendline('1')
        self.recvuntil('Enter player name:')
        self.sendline(name)
        self.sendline('1')
        self.sendline('2')
        self.sendline('3')
        self.sendline('4')
        self._wait_menu()

    def edit_player(self, name):
        # self.select_player(player_id)
        self.sendline('4')
        self._wait_menu()
        self.sendline('1')
        self.sendline(name)
        self._wait_menu()
        self.sendline('0')
        self._wait_menu()

    def select_player(self, player_id):
        self.sendline('3')
        self._wait_menu()
        self.sendline(str(player_id))
        log.info(self.recvrepeat(0.2))

    def show_player(self):
        self.sendline('5')
        output = self._wait_menu()
        return output

    def remove_player(self, player_id):
        self.sendline('2')
        self.sendline(str(player_id))
        self._wait_menu()

    def print_team(self):
        self.sendline('6')
        log.info(self.recvrepeat(0.2))
        self._wait_menu()
