import streamlit as st
import subprocess
import time
import paramiko
from paramiko import SSHClient


def load_lab(lab_option):
    if lab_option == 'Arista':
        return subprocess.run(['sudo', 'containerlab', 'deploy', '-t', 'arista.labtest.yml'], text=True, check=True, capture_output=True)

def check_run(lab_option):
    if lab_option == 'Arista':
        return subprocess.run(['sudo', 'containerlab', 'inspect', '-t', 'arista.labtest.yml'], text=True, check=True, capture_output=True)

def destroy_lab(lab_option):
    if lab_option == 'Arista':
        return subprocess.run(['sudo', 'containerlab', 'destroy', '-t', 'arista.labtest.yml'], text=True, check=True, capture_output=True)

def connect_to_device(dev_option):

    hostname = dev_option
    port = 22
    user = 'arista'
    passwd = 'arista'

    try:
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=user, password=passwd)
        while True:
            try:
                cmd = input(f'{hostname} - $> ')
                if cmd == 'exit':
                    break
                stdin, stdout, stderr = client.exec_command(cmd)
                return st.code(stdout)
                print(stdout.read().decode())
            except KeyboardInterrupt:
                break
        client.close()
    except Exception as err:
        print(std(err))