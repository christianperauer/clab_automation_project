import time
import streamlit as st
import subprocess
import json
from tinydb import TinyDB, Query
import config
import os
from pathlib import Path

db = TinyDB("labs.json", sort_keys=True, indent=4)
Labs = Query()


def get_db_labs():
    all_labs = db.all()
    lab_list = []

    for lab in all_labs:
        lab_list.append(lab['name'])

    return lab_list

def db_add_lab(lab_details):
    return db.insert(lab_details)

def db_update_lab():

    return

def db_del_lab(lab_name):
    return db.remove(Labs.name == lab_name)

def upload_lab():
    lab_file = st.file_uploader("Upload Lab File", type=["yml"])
    if lab_file is not None:
        if st.button("Upload"):
            raw_data = str(lab_file.read(), "utf-8")
            #st.write(raw_data)
            with open(os.path.join("/home/cperauer/clab-topologies", lab_file.name),"wb") as f:
                f.write(lab_file.getbuffer())
            
            st.success("Lab File Successfully Uploaded")

def lab_file_search(lab_name):
    labs_parent_dir = config.appRoot + config.labRoot
    labdb_entry_dir = db.search(Labs.name == lab_name)[0].get("localLabFolder")
    labdb_entry_file = db.search(Labs.name == lab_name)[0].get("labFile")
    return labs_parent_dir + "/" + labdb_entry_file
    
def search_lab_details(lab_name):
    return db.search(Labs.name == lab_name)

def all_lab_details():
    return db.all()

def check_lab_path(lab_path):
    '''    Check if the path entered in the lab details is valid    
    Pulls the appRoot and labRoot folders from the users config file
    Return True if valid, False if not valid    '''
    labs_parent_dir = config.appRoot + config.labRoot
    lab_full_path = f"{labs_parent_dir}/{lab_path}/"
    lab_path_check = Path(lab_full_path)
    if lab_path_check.is_dir():
        return True
    else:
        return False

def clab_function(lab_function, lab_option):
    lab_details = db.search(Labs.name == lab_option)[0]
    labs_parent_dir = config.appRoot + config.labRoot
    lab_full_path = f"{labs_parent_dir}/{lab_details['localLabFolder']}/{lab_details['labFile']}"
    lab_path_check = Path(lab_full_path)
    if lab_path_check.is_file():
        return subprocess.run(['sudo', 'containerlab', lab_function, '-t', lab_full_path], text=True, check=True, capture_output=True)
    else:
        return lab_full_path

def clab_function_des(lab_option):
    labs_parent_dir = config.appRoot + config.labRoot
    lab_details_new = db.search(Labs.labFile == lab_option)[0]
    lab_full_path = f"{labs_parent_dir}/{lab_details_new['localLabFolder']}/{lab_option}"
    lab_path_check = Path(lab_full_path)
    if lab_path_check.is_file():
        return subprocess.run(['sudo', 'containerlab', 'destroy', '-t', lab_full_path], text=True, check=True, capture_output=True)
    else:
        return lab_full_path

def get_running_labs():
    output = subprocess.run(['sudo', 'containerlab', 'inspect', '--all', '-f', 'json'], text=True, check=True, capture_output=True)
    if output.stdout == "":
        return None
    elif output.stdout != "":
        running_labs = json.loads(output.stdout)
        return running_labs 

def format_md_table():
    table_style = """
    <style>
    table:nth-of-type(1) {
        display:table;
        width:100%;
    }
    table:nth-of-type(1) th:nth-of-type(2) {
        width:65%;
    }
    </style>
    """
    return table_style


def running_lab_status(status):
    if status.lower() == "running":
        status_markdown = f"""<span style="color:green">{status}</span>"""
    else:
        status_markdown = f"""<span style="color:red">{status}</span>"""
    
    return status_markdown


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
