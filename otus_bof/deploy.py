# import time
import os
import paramiko
import shutil

def main():
    shutil.copy(os.path.expanduser("~/GOPATH/src/github.com/morentharia/gosketches/peloader/main.exe"),
                os.path.expanduser("~/hack/vmware_share/main.exe"))
    try:
        host = '192.168.149.24'
        user = 'mor'
        secret = '1'
        port = 22

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=secret, port=port)

        commands_list = [
            # Copy-Item '\\\vmware-host\\Shared Folders\\bof\\Debug\\BoF_Simple.exe' -Destination C:\\

            '''cd Z:\\bof\\Debug\\;'''
            '''Copy-Item '.\\BoF_Simple.exe' -Destination C:\\ ''',
            '''C:\\PSTools\\PsExec.exe -i 1 -s 'C:\\BoF_Simple.exe' ''',
            # '''C:\\BoF_Simple.exe''',
        ]
        for ccc in commands_list:
            stdin, stdout, stderr = client.exec_command(ccc, get_pty=True)
            data = stdout.read() + stderr.read()

            print(data.decode(errors='replace'))
            # print(data)
            print(ccc)
    except KeyboardInterrupt:
        print("bye bye")
    finally:
        # client.send(chr(3))
        channel = client.invoke_shell()
        channel.send(b'0x3')
        print("close client")
        channel.transport.close()
        client.close()

if __name__ == '__main__':
    main()
