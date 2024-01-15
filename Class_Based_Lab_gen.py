import json
import ruamel.yaml as yaml
import pprint
import sys
from pathlib import Path

## CLAB TOPOLOGY FILE DEFINITION


# Create a dictionary representing the lab name
lab_name = {}

# Create dictionaries representing the topology (that contains nodes and links)
topology = {}

# Create the rough lab file
rough_lab_file = {}

class ClabTopologyDefinition:
    # Initialize the class variables
    ## Create them using names that relate to the original variables
    def __init__(self):
        self.lab_name = {}
        self.topology = {'topology': [{'nodes':[]}, {'links':[]}]}
        self.num_nodes = int(input("Enter the number of nodes: "))
        self.name = input("Enter the Lab Topology name (No Spaces, only '_' allowed): ")
        self.txt_file_name = input("Enter the Lab File Name (No Spaces, only '_' allowed): ")

        # Defining initial Eth values to connect interfaces later on
        self.local_eth = 1
        self.remote_eth = 1
        self.current_link = 1
        self.current_node = 1
        self.total_links = self.num_nodes - 1

    # Declare method to validate if the lab name input is valid format
    def is_valid_lab_name(self):
        if not self.name or " " in self.name or not all (char.isalnum() or char == "_" for char in self.name):
            return False
        else:
            return True
        
    # Declare method to valiate if the lab file name input is valid format
    def is_valid_lab_file_name(self):
        if not self.txt_file_name or " " in self.txt_file_name or not all (char.isalnum() or char == "_" for char in self.txt_file_name):
            return False
        else:
            return True         


class GenerateTopologyName(ClabTopologyDefinition):
    # Declare method that take the user defined lab name and puts it in file
    def create_lab_topology_name(self):
        if self.is_valid_lab_name() == True:  # Don't pass self here
            self.lab_name = {"name": str(f"{self.name}")}
            return self.lab_name
        else:
            return "Invalid name. Please try again."


class CreateTopoLinks(GenerateTopologyName):
        # Verify correct number of device - Minimun 2 and Max 20
        def create_topology_links(self):
            if self.num_nodes < 2 or self.num_nodes > 20:
                return "Number of supported devices 2-20. Please select try again."
            else:
                # Iterate through the number of selected nodes, create and append to list
                    for node_c in range(1, self.num_nodes + 1):
                        self.node_name = str(f"ceos{node_c}")
                        self.node_c = { self.node_name: {
                            'kind': 'ceos',
                            'image': 'h4ndzdatm0ld/ceosimage:4.28.0F'
                            }
                        }
                        self.topology['topology'][0]['nodes'].append(self.node_c)

                        # Building connecting links
                        self.node_count = 1

                        # Verifying if Total Links and Total Nodes Ration checks
                        if self.current_link <= self.total_links:
                            self.topology['topology'][1]['links'].append(
                                {'endpoints': [
                                    f"ceos{self.current_node}:eth{self.current_link}", 
                                    f"ceos{self.current_node + 1}:eth{self.current_link}"
                                ]}
                            )
                        
                        # Changing Link and Node Count
                        self.current_node += 1
                        self.current_link += 1

                        # Changing connecting devices
                        self.local_eth += 1
                        self.remote_eth += 1
                        self.node_count += 1
            
            return self.topology


class CreateAndModifyFiles(CreateTopoLinks):
    # Create a new TXT file to store the generated lab data that will be then transformed to YML
    def create_and_modify_files(self):
        # If Lab File has a Valid name: combine Lab name dict and topology dict
        self.txt_lab_file = self.lab_name | self.topology
        if self.is_valid_lab_file_name():
            with open(self.txt_file_name + ".txt", "w") as yaml_file:
                yaml.dump(self.txt_lab_file, yaml_file, Dumper=yaml.RoundTripDumper, default_flow_style=False)
                return "Success"
        else:
            return "There was an issue with the Lab File Name, please try again."


class RefactorTxtIntoYaml(CreateAndModifyFiles):
    # Define method to reformat TXT into YAML
    def reformat_yaml_txt(self):
        # Open and read Text file
        with open(self.txt_file_name + ".txt", "r+") as self.txt_file:
            self.disp_data = self.txt_file.readlines()
            self.disp_data_new = []

            self.counter = 0

            for line in self.disp_data:
                if 'nodes' in line or 'links' in line:
                    line = line.replace('-', '')
                elif 'ceos' in line and 'eth' not in line:
                    line = line.replace('-', '')
                self.disp_data_new.append(line)
                self.counter += 1

        # Reopening the file with "W" flag instead of "R" so we avoid using Truncate file so ew dont get the Byte error
        with open(self.txt_file_name + ".txt", "w") as self.txt_file:
            self.txt_file.writelines(self.disp_data_new)

        self.p = Path(self.txt_file_name + ".txt")
        self.p.rename(self.p.with_suffix('.yml'))


# topology_links = CreateTopoLinks()

# lab_name = topology_links.create_lab_topology_name()

# topology = topology_links.create_topology_links()


topology_links = RefactorTxtIntoYaml()

lab_name = topology_links.create_lab_topology_name()

topology = topology_links.create_topology_links()

create_file = topology_links.create_and_modify_files()

c_and_m_file = topology_links.reformat_yaml_txt()

# print()
# print(lab_name)
# print()
# print(topology)
# print()

