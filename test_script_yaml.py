import ruamel.yaml as yaml
import pprint
import re
# import yaml


# Create a dictionary representing the lab name
lab_name = {}

# Create dictionaries representing the topology (that contains nodes and links)
topology = {'topology': [{'nodes':[]}, {'links':[]}]}

# Define the number of nodes
num_nodes = int(input("Enter the number of nodes: "))

# Define the LAB name
# Creating a Function that Verifies Lab valid name or not
def is_valid_lab_name(name):
    if name is None:
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


# Defining initial Eth values for connecting interfaces
local_eth = 1
remote_eth = 1

# Verify correct number of device - Minimun 2 and Max 20
if num_nodes < 1 or num_nodes > 20:
    print("Please pick a number of devices between 2 and 20")
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
        topology['topology'][1]['links'].append(
            {'endpoints': [
                f"{node_name}:eth{local_eth}", f"ceos{node_count + 1}:eth{remote_eth}"
            ]
            }
        )

        # Changing connecting devices
        local_eth += 1
        remote_eth += 1
        node_count += 1

# Define the finished lab file to dump into YAML
lab_file = lab_name | topology

# Create a YAML file
with open("dynamic_topology.txt", "w") as yaml_file:
    yaml.dump(lab_file, yaml_file, Dumper=yaml.RoundTripDumper, default_flow_style=False)

pprint.pprint(lab_file)



    
        