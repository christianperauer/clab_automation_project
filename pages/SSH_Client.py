import paramiko
import time

hostname = '172.20.20.2'
port = 22
user = 'admin'
passwd = 'admin'

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=user, password=passwd)
    connection.send("enable\n")
    time.sleep(1)
    connection.send("admin\n")
    time.sleep(1)
    while True:
        try:
            cmd = input(f'{hostname} - $> ')
            if cmd == 'exit': break
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
        except KeyboardInterrupt:
            break
    client.close()
except Exception as err:
    print(std(err))