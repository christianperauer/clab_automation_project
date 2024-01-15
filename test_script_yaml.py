# Testing NEW Multi Topology CODE - TEST 1

import ruamel.yaml as yaml
import pprint
import sys
from pathlib import Path


# Defining required variables for Multi Topology new version
is_core = False
is_linear = False


# Print the Topology Menu with Options
print('''
      
=======================================
| Select Topology Type:               |
|        1) Linear                    |
|        2) Core                      |
|        3) Fabric / Spine and Leaf   |
|                                     |
|                                     |
=======================================

''')


# User's Choice of Topology Type
topology_type = int(input("Enter the Topology Type: "))


## UTILS CANDIDATE
# Adding File Formatting and Renaming Function
def reformat_yaml_txt(file):
# Open and read Text file
    with open(file, "r+") as txt_file:
        disp_data = txt_file.readlines()
        disp_data_new = []

        counter = 0

        for line in disp_data:
            if 'nodes' in line or 'links' in line:
                line = line.replace('-', '')
            elif 'ceos' in line and 'eth' not in line:
                line = line.replace('-', '')
            disp_data_new.append(line)
            counter += 1


    # Reopening the file with "W" flag instead of "R" so we avoid using Truncate file so ew dont get the Byte error
    with open("dynamic_topology.txt", "w") as txt_file:
        pass
        txt_file.writelines(disp_data_new)

    p = Path("dynamic_topology.txt")
    p.rename(p.with_suffix('.yml'))



## UTILS CANDIDATE
# Adding Function to exit program for completeness
def exit_program():
    print("Exiting the Program...")
    sys.exit(0)

# Create a dictionary representing the lab name
lab_name = {}

# Create dictionaries representing the topology (that contains nodes and links)
topology = {'topology': [{'nodes':[]}, {'links':[]}]}


## UTILS CANDIDATE
# Define the number of nodes WITH ENHANCEMENT FOR MUTI TOPOLOGY

def topology_selector(selection):
    if selection == 3:
        is_linear = False
        is_core = False
        # CLAB GENERATE COMMAND SCENARIO - TO BE CODED
        print("This solution needs to still be coded - Work In Progress")
    elif selection == 1:
        is_linear = True
        is_core = False
        num_nodes = int(input("Enter the number of nodes: "))
        # Defining initial Eth values for connecting interfaces
        local_eth = 1
        remote_eth = 1
        current_link = 1
        current_node = 1
        total_links = num_nodes - 1

        # Verify correct number of device - Minimun 2 and Max 20
        if num_nodes < 1 or num_nodes > 20:
            print("Please pick a number of devices between 2 and 20")
            exit_program()
        else:
            # Iterate through the number of selected nodes, create and append to list
            for node_c in range(1, num_nodes + 1):
                node_name = str(f"ceos{node_c}")
                node_c = { node_name: {
                    'kind': 'ceos',
                    'image': 'h4ndzdatm0ld/ceosimage:4.28.0F'
                    }
                }
                topology['topology'][0]['nodes'].append(node_c)

                # Building connecting links
                node_count = 1

                # Verifying if Total Links and Total Nodes Ration checks
                if current_link <= total_links:
                    topology['topology'][1]['links'].append(
                        {'endpoints': [
                            f"ceos{current_node}:eth{current_link}", 
                            f"ceos{current_node + 1}:eth{current_link}"
                        ]
                        }
                    )

                # Changing Link and Node Count
                current_node += 1
                current_link += 1

                # Changing connecting devices
                local_eth += 1
                remote_eth += 1
                node_count += 1

    elif selection == 2:
        is_linear = False
        is_core = True
        num_edge_nodes = int(input("Enter the number of EDGE nodes: "))
        num_mid_nodes = int(input("Enter the number of MID nodes: "))
        num_dh_nodes = int(input("Enter the number of DH nodes: "))
        return is_linear, is_core, num_edge_nodes, num_mid_nodes, num_dh_nodes


## UTILS CANDIDATE
# Define the LAB name
# Creating a Function that Verifies Lab valid name or not
def is_valid_lab_name(name):
    if name == '':
        return False
    elif name is None:
        return False
    elif " " in name:
        return False
    elif not all(char.isalnum() or char == "_" for char in name):
        return False
    return True

# Prompt users for input until valid name is provided
while True:
    lab_name_input = input("Enter the Lab Topology name (No Spaces, only '_' allowed): ")
    if is_valid_lab_name(lab_name_input):
        lab_name = {"name":str(f"{lab_name_input}")}
        break
    else:
        print("Invalid name. Please try again.")


# Calling Topology Type and Generation Function
topology_selector(topology_type)


# Define the finished lab file to dump into YAML
lab_file = lab_name | topology

# Create a YAML file
with open("dynamic_topology.txt", "w") as yaml_file:
    yaml.dump(lab_file, yaml_file, Dumper=yaml.RoundTripDumper, default_flow_style=False)

# Print Statement if needed to visualize generated file for testing
# Commment if not needed
# pprint.pprint(lab_file)


# Adding Final Line to complete the process for file reformatting and renaming
reformat_yaml_txt("dynamic_topology.txt")

    
        