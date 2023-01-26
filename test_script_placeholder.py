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

pprint.pprint(running_labs)

lab_list = []
lab_dev_list = []
dev_ip_list = []

for lab in running_labs['containers']:
    if lab['name'] not in lab_dev_list and lab['ipv4_address'] not in dev_ip_list:
        lab_dev_list.append(lab['name'])
        dev_ip_list.append(lab['ipv4_address'][:-3])
        if lab['lab_name'] not in lab_list:
            lab_list.append(lab['lab_name'])


print(lab_list)
print(lab_dev_list)
print(dev_ip_list)

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


if __name__ == "__main__":
    get_running_labs()