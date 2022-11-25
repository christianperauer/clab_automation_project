import streamlit as st
import subprocess

def load_lab(lab_option):
    if lab_option == 'Arista':
        return subprocess.run(['sudo', 'containerlab', 'deploy', '-t', 'arista.labtest.yml'], text=True, check=True, capture_output=True)

def check_run(lab_option):
    if lab_option == 'Arista':
        return subprocess.run(['sudo', 'containerlab', 'inspect', '-t', 'arista.labtest.yml'], text=True, check=True, capture_output=True)

def destroy_lab(lab_option):
    if lab_option == 'Arista':
        return subprocess.run(['sudo', 'containerlab', 'destroy', '-t', 'arista.labtest.yml'], text=True, check=True, capture_output=True)
