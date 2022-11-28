import paramiko
import time

# Connection Parameters

device = '172.20.20.2'
user_name = 'admin'
passwd = 'admin'
enable_passwd = 'admin'
port = 22

try:
    # Create SSH Client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device, username=user_name, passwrd=passwd)
    print('Successfully Connected to %s' % device)

    remote_conn = ssh.invoke_shell()
    output = remote_conn.recv(5000)

    # Access device privileged mode and disable Paging on Remote Device
    remote_conn.send('terminal length 0\n')
    remote_conn.send('enable\n')
    time.sleep(2)
    if remote_conn.recv_ready() and 'password' in remote_conn.recv(5000):
        remote_conn.send(enable_passwd)
    else:
        # output = remote_conn.recv(65000)
        print(output)

    # Create Loop fo CLI Client Exec
    while True:
        try:
            cmd = input(f'{device} - #> ')
            if cmd == 'exit':
                break
            elif remote_conn.recv_ready():
                # Sending the CLI command
                remote_conn.send(cmd)
                time.sleep(2)
                # Getting the output
                output = remote_conn.recv(65000)
                print(output)
            else:
                print('Error Check')
        except KeyboardInterrupt:
            break
except:
    pass