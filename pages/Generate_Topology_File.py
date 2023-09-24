import streamlit as st
import yaml
import utils
import json
import config
from git import Repo
import os
from pathlib import Path
from tinydb import TinyDB, Query


st.title("CLAB Topology File Generator")

# Create a form to collect user input
name = st.text_input("Name")
ceos_count = st.number_input("Number of ceos nodes", min_value=1, step=1)

ceos_nodes = {}
for i in range(ceos_count):
    node_name = st.text_input(f"Node {i+1} Name")
    node_image = st.text_input(f"Node {i+1} Image")
    ceos_nodes[node_name] = {
        "kind": "ceos",
        "image": node_image
    }

link_endpoints = st.multiselect("Link Endpoints (format: 'node:interface')", ceos_nodes.keys(), key="link")

if st.button("Generate YAML"):
    topology = {
        "nodes": ceos_nodes,
    }

    # Add the Links section to the topology at the end

    topology["links"] = [{"endpoints": [f"{endpoint}:eth1" for endpoint in link_endpoints]}]

    yaml_data = {
        "name": name,
        "topology": topology
    }

    with open("output.yaml", "w") as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False)

    st.success("YAML file generated successfully!")

# Optionally, you can display the generated YAML file
if st.checkbox("Display Generated YAML File"):
    with open("output.yaml", "r") as yaml_file:
        yaml_content = yaml_file.read()
        st.text_area("Generated YAML File", yaml_content, height=400)
