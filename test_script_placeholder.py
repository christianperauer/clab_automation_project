# import time
# import streamlit as st
# import subprocess
# import json
# from tinydb import TinyDB, Query
# import config
# import os
# from pathlib import Path
# import pprint
# import re

# db = TinyDB("labs.json")
# Labs = Query()

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


# if __name__ == "__main__":
#     get_running_labs()


# import yaml
# import ruamel.yaml
# import sys

# name = "LAB TEST1"

# virtual_nodes = {}
# dev_connections = {"endpoints": []}

# endpoint_pri = []
# endpoint_sec = []

# num_of_nodes = int(input("Enter the number of lab nodes: "))

# while len(virtual_nodes) < num_of_nodes:
#     selected_node = input(f"Enter the name of Endpoint {len(virtual_nodes)}: ")
#     Selected_port = input(f"Enter the name of Endpoint Interface {len(virtual_nodes)}: ")
#     selected_kind = input(f"Enter the Device Kind of Endpoint {len(virtual_nodes)}: ")
#     selected_image = input(f"enter the image for Endpoint {len(virtual_nodes)}: ")
#     virtual_nodes[selected_node] = {"kind": selected_image, "image": selected_image}
#     dev_connections["endpoints"].append(f"{selected_node}:{Selected_port}")
    # print(len(virtual_nodes))

# print(virtual_nodes)
# print(links)

# Format the dictionary manually
# yaml_str = "- endpoints: " + str(dev_connections["endpoints"])

# topology = {"nodes":virtual_nodes}

# yaml_data = {"links": yaml_str, "name": name, "topology": topology}

# print(yaml.dump(yaml_data, default_flow_style=False))

# ----------------------------------------------------------------------

# '''
# # Create the dictionary
# links = {
#     "endpoints": ["upload-ceos01:eth1", "upload-ceos02:eth1"]
# }

# # Format the dictionary manually
# yaml_str = "- endpoints: " + str(links["endpoints"])

# # Save the YAML data to a file
# with open("output.yaml", "w") as yaml_file:
#     yaml_file.write(yaml_str)

# print(yaml_str)

# '''


# import pprint
# import ruamel.yaml as yaml

# # Create an ordered dictionary representing the lab name
# lab_name = yaml.comments.CommentedMap()
# lab_name['name'] = yaml.comments.CommentedSeq()

# # Create an ordered dictionary representing the topology
# topology_dict = yaml.comments.CommentedMap()
# topology_dict['topology'] = yaml.comments.CommentedSeq()
# topo_dict = yaml.comments.CommentedMap()
# topo_dict['nodes'] = yaml.comments.CommentedSeq()
# topo_dict['links'] = yaml.comments.CommentedSeq()

# # Define the number of nodes
# num_nodes = int(input("Enter the number of nodes: "))

# # Define the LAB name
# # Creating a Function that Verifies Lab valid name or not
# def is_valid_lab_name(name):
#     if name is None:
#         return False
#     elif " " in name:
#         return False
#     elif not all(char.isalnum() or char == "_" for char in name):
#         return False
#     return True

# # Prompt users for input until valid name is provided

# while True:
#     lab_name_input = input("Enter the Lab Topology name (No Spaces, only '_' allowed): ")
#     if is_valid_lab_name(lab_name_input):
#         lab_name = {"name":str(f"{lab_name_input}")}
#         break
#     else:
#         print("Invalid name. Please try again.")


# # Generate nodes and links
# for i in range(1, num_nodes + 1):
#     node_name = str(f"ceos{i}")
#     node = {
#         node_name: {
#         "kind": "ceos",
#         "image": "device/image"
#         }
#     }
#     topo_dict['nodes'].append(node)

#     if i > 1:
#         link = {
#             "endpoints": str([f"{node_name}:eth1", f"ceos{i-1}:eth1"]),
#         }
#         topo_dict['links'].append(link)


# # Integrating Nodes List Dictionary into Main Topology Dictionary
# topology_dict = {'topology': [{'nodes': topo_dict['nodes']}]}


# # Loop through LINKS dictionary and refactor links to CLAB format
# for item in topo_dict['links']:
#     if 'endpoints' in item:
#         value = item['endpoints']
#         if isinstance(value, str):
#             # Remove single quotes and replace square brackets with lists
#             updated_value = eval(value.replace("'", '"'))
            
#             # Update the original dictionary with the modified value
#             item['endpoints'] = updated_value


# # Integrating Nodes List Dictionary into Main Topology Dictionary
# topology_dict['links'] = list(topo_dict['links'])


# # Append both Dictionaries, Name and Topology into the same YAML file
# lab_file = lab_name | topology_dict

# pprint.pprint(lab_file)


# # Create a YAML file
# with open("dynamic_topology.yaml", "w") as yaml_file:
#     yaml.dump(lab_file, yaml_file, Dumper=yaml.RoundTripDumper, default_flow_style=False)


# print("--------------------------------------------")
# print("Dynamic topology file created successfully")
# print("--------------------------------------------")
# print()
# print("--------------------------------------------")
# print("Refactoring YAML File Format...")
# print("--------------------------------------------")
# print()


# # Open YAML File created above to be refactored to CLAB acceptable format
# with open("dynamic_topology.yaml", "r") as yml_file:
#     disp_data = yaml.safe_load(yml_file)
    # print(disp_data[0])
    # print(disp_data[1]['links'])
    # print(type(disp_data[1]['links']))
    # print(type(disp_data[1]))


# # Modify the data structure to remove "-" from "name," "topology," and "nodes"
# if 'name' in disp_data:
#     disp_data['name'] = disp_data['name']

# if 'topology' in disp_data:
#     topology = disp_data['topology']
#     if 'nodes' in topology:
#         nodes = topology['nodes']
#         for node in nodes:
#             for key, value in node.items():
#                 nodes[nodes.index(node)][key] = value


# # Write the modified data back to the YAML file
# with open('dynamic_topology.yaml', 'w') as file:
#     yaml.dump(disp_data, file, default_flow_style=False)

import itertools

edge_count = int(input("Enter the total number of edges: "))

mid_count = int(input("Enter the total number of mid devices: "))

right_edge = []
left_edge = []
right_list = []
left_list = []
edge_devices = []
mid_devices = []
top_mids = []
bottom_mids = []

is_core = True

# if edge_count > 3 and edge_count %2 == 0 and is_core == True:
#     print(edge_count)
#     left_list = [f"ceos{node}" for node in range(1, edge_count + 1) if node %2 == 0]
#     right_list = [f"ceos{node}" for node in range(1, edge_count) if node %2 != 0]
# elif edge_count %2 != 0:
#     print("Please select an even number of Edges")

edge_devices = [f"ceos-pe{node}" for node in range(1, edge_count + 1) if node > 0]
left_list = edge_devices[0::2]
right_list = edge_devices[1::2]

mid_devices = [f"ceos-p{node}" for node in range(1, mid_count + 1) if node > 0]
top_mids = mid_devices[0::2]
bottom_mids = mid_devices[1::2]




print("EDGE DEVICES")
print("-"*len("EDGE DEVICES"))
print()
print(edge_devices)
print()
print("EDGE LEFT")
print("-"*len("EDGE LEFT"))
print()
print(left_list)
print()
print("EDGE RIGHT")
print("-"*len("EDGE RIGHT"))
print()
print(right_list)
print()
print("MID DEVICES")
print("-"*len("MID DEVICES"))
print()
print(mid_devices)
print()
print("TOP MIDS")
print("-"*len("TOP MIDS"))
print()
print(top_mids)
print()
print("BOTTOM MIDS")
print("-"*len("BOTTOM MIDS"))
print()
print(bottom_mids)

## LINKS DEFINITION

per_pr = []
peb_pb = []
per_pb = []
peb_pr = []
pr_pb = []
pb_pr = []
pr_pr = []
pb_pb = []


# print()
# print()
# print(len(top_mids))
# print(top_mids)
# print(len(bottom_mids))
# print(bottom_mids)
# print(len(left_list))
# print(left_list)
# print(len(right_list))
# print(right_list)
# print()


# Deconstruct List Comprehension

intf_num = 1


# Scenario with only 1 PR and 2 PER
def building_per_to_pr_one_pr():
    if len(top_mids) == 1 and len(left_list) >= 2 and len(right_list) >= 2:
        for (top_node,bottom_node) in zip(left_list,right_list):
            if top_node == left_list[0]:
                per_pr.append(f"{left_list[0]}:eth{intf_num}, {top_mids[0]}:eth{intf_num}")
            elif top_node == left_list[-1]:
                per_pr.append(f"{left_list[-1]}:eth{intf_num+1}, {top_mids[0]}:eth{intf_num+1}")
    return per_pr


# Scenario with only 1 PB and 2 PEB
def building_peb_to_pb_one_pb():
    if len(bottom_mids) == 1 and len(left_list) >= 2 and len(right_list) >= 2:
        for (top_node,bottom_node) in zip(left_list,right_list):
            if bottom_node == right_list[0]:
                peb_pb.append(f"{right_list[0]}:eth{intf_num}, {bottom_mids[0]}:eth{intf_num}")
            elif bottom_node == right_list[-1]:
                peb_pb.append(f"{right_list[-1]}:eth{intf_num+1}, {bottom_mids[0]}:eth{intf_num+1}")
    return peb_pb


# Scenario with 2 or more PRs and 2 PER
def building_per_to_pr_two_more_pr():
    if len(top_mids) >= 2 and len(left_list) >= 2 and len(right_list) >= 2:
        for (top_node,bottom_node) in zip(left_list,right_list):
            if top_node == left_list[0]:
                per_pr.append(f"{left_list[0]}:eth{intf_num}, {top_mids[0]}:eth{intf_num}")
            elif top_node == left_list[-1]:
                per_pr.append(f"{left_list[-1]}:eth{intf_num+1}, {top_mids[-1]}:eth{intf_num+1}")
    return per_pr


# Scenario with 2 or more PBs and 2 PEB
def building_peb_to_pb_two_more_pb():
    if len(top_mids) >= 2 and len(left_list) >= 2 and len(right_list) >= 2:
        for (top_node,bottom_node) in zip(left_list,right_list):
            if bottom_node == right_list[0]:
                peb_pb.append(f"{right_list[0]}:eth{intf_num}, {bottom_mids[0]}:eth{intf_num}")
            elif bottom_node == right_list[-1]:
                peb_pb.append(f"{right_list[-1]}:eth{intf_num+1}, {bottom_mids[-1]}:eth{intf_num+1}")
    return peb_pb


if edge_count >= 4 and mid_count <= 2:
    building_per_to_pr_one_pr()
    building_peb_to_pb_one_pb()
elif edge_count >= 4 and mid_count > 2:
    building_per_to_pr_two_more_pr()
    building_peb_to_pb_two_more_pb()


print()
print("PER To PR Links")
print(len("PER To PR Links")*"-")
print()
print(per_pr)
print()
print("PEB To PB Links")
print(len("PEB To PB Links")*"-")
print()
print(peb_pb)
print()
