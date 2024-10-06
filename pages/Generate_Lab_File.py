"""
Author: Christian D Perauer (CDP)
Date: 2024-07-25

Description:
    This script is designed to test "Containerlab" dynamic/customized topology files in YAML format, 
    to be directly consumed by Containerlab

Purpose:
    The primary purpose of this script is to automate the CLAB topology file generation requires to point 
    to whenever a new lab is needed

Usage:
    - To use this script, ensure you have Python 3.8.10 installed 
    - Install necessary libraries listed in the requirements.txt
    - Run the script using the command: python Generate_Lab_Files.py

Sections:
    1. Imports: Contains all necessary import statements
    2. Functions: Contains all function definitions used in the script
    3. Main Execution: The main execution block that orchestrates the script's workflow
    4. Form Test: Page Section for "st.form" testing

Notes:
    - Ensure that the generated file is placed in the correct directory 
    - This script is intended for use by the data analysis team within the sales department.

Contact:
    For any questions or issues, please contact cperauer@bcnnetworks.com or refer to the project's GitHub 
"""

## IMPORTS

import ruamel.yaml as yaml
import pprint
import sys
from pathlib import Path
import streamlit as st
import yaml
import utils
import json
import config
from git import Repo
import os
from tinydb import TinyDB, Query

## This Page will be used as testing bed for "Dynamic Topology" file generstion task

## FORM TEST

### Creating page Header as H1 HTML element
st.markdown("<h1>Enter the Lab Details</h1>", unsafe_allow_html=True)

### Creating Streamlit Form for users to provide lab details input
form = st.form("Lab Details")
form.text_input("Number of Devices")
form.form_submit_button("Create")