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

def send_cmd(conn, command):
    """
    Given an open connection and a command, issue the command and wait one second for the command to be processed
    """
    conn.send(command + "\n")
    time.sleep(1.0)

def get_output(conn):
    """
    Given an open connection, read all the data from the buffer and decode the byte string as UTF-8
    """
    return conn.recv(65535).decode()