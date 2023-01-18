import time
import streamlit as st
import subprocess
import json
from tinydb import TinyDB, Query
import config
import os
from pathlib import Path
import pprint

db = TinyDB("labs.json")
Labs = Query()

output = subprocess.run(['sudo', 'containerlab', 'inspect', '--all', '-f', 'json'], text=True, check=True, capture_output=True)
# print(output.stdout)
# print(type(output))
# print(type(output.stdout))

# test = output.stdout == ""
# print(test)

def get_running_labs():
    output = subprocess.run(['sudo', 'containerlab', 'inspect', '--all', '-f', 'json'], text=True, check=True, capture_output=True)
    if output.stdout == "":
        return {'null': None}
    elif output.stdout != "":
        running_labs = json.loads(output.stdout)
        #pprint.pprint(running_labs)
        return running_labs

running_labs = get_running_labs()

run_labs_list = []
if running_labs is None:
    print('There are no Labs running')
elif running_labs is not None:
    for lab in running_labs['containers']:
        if lab['labPath'] not in run_labs_list:
            run_labs_list.append(lab['labPath'])
print (run_labs_list)

dest_all_labs = db.all()
dest_lab_list = []
for lab in dest_all_labs:
    if lab['labFile'] not in dest_lab_list:
        dest_lab_list.append(lab['labFile'])
print(dest_lab_list)

dest_final_list = []
for file in dest_lab_list:
    if file in run_labs_list:
        dest_final_list.append(file)
print(dest_final_list)


if __name__ == "__main__":
    get_running_labs()