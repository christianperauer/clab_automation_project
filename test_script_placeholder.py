import time
import streamlit as st
import subprocess
import json
from tinydb import TinyDB, Query
import config
import os
from pathlib import Path
import pprint
import re
from git import Repo
import utils
import socket


db = TinyDB("labs.json")
Labs = Query()

# output = subprocess.run(['sudo', 'containerlab', 'inspect', '--all', '-f', 'json'], text=True, check=True, capture_output=True)
# # print(output.stdout)
# # print(type(output))
# # print(type(output.stdout))

# # test = output.stdout == ""
# # print(test)

# def get_running_labs():
#     output = subprocess.run(['sudo', 'containerlab', 'inspect', '--all', '-f', 'json'], text=True, check=True, capture_output=True)
#     if output.stdout == "":
#         return {'null': None}
#     elif output.stdout != "":
#         running_labs = json.loads(output.stdout)
#         #pprint.pprint(running_labs)
#         return running_labs

# running_labs = get_running_labs()

# pprint.pprint(running_labs)

# lab_list = []
# lab_dev_list = []
# dev_ip_list = []

# for lab in running_labs['containers']:
#     if lab['name'] not in lab_dev_list and lab['ipv4_address'] not in dev_ip_list:
#         lab_dev_list.append(lab['name'])
#         dev_ip_list.append(lab['ipv4_address'][:-3])
#         if lab['lab_name'] not in lab_list:
#             lab_list.append(lab['lab_name'])


# print(lab_list)
# print(lab_dev_list)
# print(dev_ip_list)

# run_labs_list = []
# if running_labs is None:
#     print('There are no Labs running')
# elif running_labs is not None:
#     extrLabFromPath = re.compile(r'\S+\/\S+\/(\S+)')
#     for lab in running_labs['containers']:
#         lab_match_ob = extrLabFromPath.search(lab['labPath'])
#         if lab_match_ob.group(1) not in run_labs_list:
#             run_labs_list.append(lab_match_ob.group(1))
#             print (run_labs_list)

# dest_all_labs = db.all()
# dest_lab_list = []
# for lab in dest_all_labs:
#     if lab['labFile'] not in dest_lab_list:
#         dest_lab_list.append(lab['labFile'])
# print(dest_lab_list)

# dest_final_list = []
# for file in dest_lab_list:
#     if file in run_labs_list:
#         dest_final_list.append(file)
# print(dest_final_list)

# def lab_clone():
#     git_url = 'https://github.com/christianperauer/clab_automation_project.git'
#     labs_parent_dir = config.appRoot + config.labRoot
#     repo_dir = ''
#     repo_path = Path(labs_parent_dir + repo_dir)
#     repo_git = Path(labs_parent_dir + repo_dir + ".git")
#     if repo_path.is_dir():
#         print("Warning Path already exists, checking for existing git repo")
#         if repo_git.is_file():
#             print("Git repo already in this directory, delete it before trying again")
#             print(repo_git)
#         else:
#             print(f"Cloning repo from {git_url}")
#             Repo.clone_from(git_url, labs_parent_dir + repo_dir)
#             print(repo_git)
#             print(repo_path)
#             print(labs_parent_dir)
#     else:
#         print(f"Making directory {repo_path}")
#         os.mkdir(labs_parent_dir + repo_dir)
#         print(f"Cloning repo from {git_url}")
#         Repo.clone_from(git_url, labs_parent_dir + repo_dir)

# labs_parent_dir = Path(config.appRoot + config.labRoot)

# if labs_parent_dir.is_dir():
#     print(labs_parent_dir)
#     print(type(labs_parent_dir))
# else:
#     print('Try Again')



# def test_topo_map(lab_option):
    # labs_list = utils.get_db_labs()
    # print("")
    # lab_option = input("Enter Lab Option: ")
    # print("")
    # lab_function = input("Enter Function Option: ")
    # print("")
    # lab_details = db.search(Labs.name == lab_option)[0]
    # print("")
    # labs_parent_dir = config.appRoot + config.labRoot
    # lab_full_path = f"{labs_parent_dir}/{lab_details['localLabFolder']}/{lab_details['labFile']}"
    # lab_path_check = Path(lab_full_path)
    # print("")
    # if lab_path_check.is_file():
    #     return subprocess.run(['sudo', 'containerlab', lab_function, '-t', lab_full_path], text=True, check=True, capture_output=True)
    # else:
    #     return lab_full_path

    # running_labs = utils.get_running_labs()
    # run_labs_list = []
    # if running_labs is None:
    #     print('There are no Labs running')
    #     st.error('There are no Labs running', icon="⚠️")
    # elif running_labs is not None:
    #     extrLabFromPath = re.compile(r'\S+\/\S+\/(\S+)')
    #     for lab in running_labs['containers']:
    #         lab_match_ob = extrLabFromPath.search(lab['labPath'])
    #         if lab_match_ob.group(1) not in run_labs_list:
    #             run_labs_list.append(lab_match_ob.group(1))
    #             st.write(run_labs_list)

    # dest_all_labs = db.all()
    # dest_lab_list = []
    # for lab in dest_all_labs:
    #     if lab['labFile'] not in dest_lab_list:
    #         dest_lab_list.append(lab['labFile'])
    #         st.write(dest_lab_list)

    # dest_final_list = []
    # for file in dest_lab_list:
    #     if file in run_labs_list:
    #         dest_final_list.append(file)
    #         st.write(dest_final_list)

    # st.write("Select Lab to Destroy")
    # option = st.selectbox(
    #     'Select a lab:', dest_final_list
    # )
    # print(dest_final_list)
    # lab_shutdown = st.form_submit_button("Destroy")


### LATEST TESTING ON CLAB GRAPH


    # labs_parent_dir = config.appRoot + config.labRoot
    # lab_details_new = db.search(Labs.labFile == lab_option)[0]
    # lab_full_path = f"{labs_parent_dir}/{lab_details_new['localLabFolder']}/{lab_option}"
    # lab_path_check = Path(lab_full_path)
    # if lab_path_check.is_file():
    #     test_output = subprocess.Popen(['sudo', 'containerlab', 'graph', '-t', lab_full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     stdout, stderr = test_output.communicate()
    #     if test_output.returncode == 0:
    #         print(f'stdout: {stdout.decode()}')
    #     else:
    #         print(f'stderr: {stderr.decode()}')
    #         print('50080: bind: address already in use' in stderr.decode())
    # else:
    #     print(lab_full_path)

    # host = '10.10.0.12'
    # port = 50080

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.settimeout(5)

    # try:
    #     result = s.connect_ex((host, port))
    #     if result == 0:
    #         print(f"Connection to {host}:{port} established.")
    #         s.close()
    #     else:
    #         print(f"Unable to connect to {host}:{port}.")
    # except socket.timeout:
    #     print(f"Timeout error when connecting to {host}:{port}.")
    # except Exception as e:
    #     print(f"Error when connecting to {host}:{port}: {e}")

    # s.close()


# if __name__ == "__main__":
#     test_topo_map('ceos-evpn-overlaid.clab.yml')
#     # test_topo_map()

# def test_fun():
#     result = subprocess.run(["sudo", "lsof", "-ti", "tcp:50080"], stdout=subprocess.PIPE)
#     pid = result.stdout.strip()
#     return pid
#     print(pid)
#     print(type(pid))

# test_fun()


def clab_function(lab_option):
    lab_details = db.search(Labs.name == lab_option)[0]
    labs_parent_dir = config.appRoot + config.labRoot
    lab_full_path = f"{labs_parent_dir}/{lab_details['localLabFolder']}/{lab_details['labFile']}"
    lab_path_check = Path(lab_full_path)
    if lab_path_check.is_file():
        print('')
        print(lab_details)
        print('')
        print(type(lab_details))
        print('')
        print(lab_details['labFile'])
        print('')
        # return subprocess.run(['sudo', 'containerlab', lab_function, '-t', lab_full_path], text=True, check=True, capture_output=True)
    else:
        print(lab_full_path)



if __name__ == "__main__":
    clab_function('Arista 2 Device Test Lab 1')