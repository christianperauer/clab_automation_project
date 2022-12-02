import streamlit as st
import os
import subprocess
#import requests

"""
# WELCOME TO LAB GENERATOR

The very fisrt dynamic Lab generator

The tool provides 2 options:

* Spin up pre-defined labs
* Spin up an on demand custom lab

Supported Vendors so far

* Cisco (IOS-XE and IOS-XR)
* Arista cEOS
* Nokia SRL

"""

pre_defined_total = 0

name = st.text_input('Enter your name: ')

option = st.selectbox(
    'What would like to do:', ('', 'Use a pre-defined Lab', 'Create a new custom Lab', 'Other')
)



def take_action(opt):
    #lab_spinup_cmd = f'containerlab deploy -t {lab_file}'
    #lab_cmd_temp = subprocess.Popen([lab_spinup_cmd], stdout= subprocess.PIPE)
    if opt == 'Use a pre-defined Lab':
        lab_option = st.selectbox(
        'Which lab would you like to use?', ('OSPF Lab', 'BGP Lab', 'Failover Lab', 'Arista Lab'))
        if lab_option == 'Arista Lab':
            temp = subprocess.run('containerlab deploy -t arista.labtest.yml', stdout=subprocess.PIPE, text=True, shell=True)
            output = temp.returncode
            if output == 0:
                return f'Successfully Creating {lab_option}' # ADD BUTTON TO SHOW RUNNING LABS AND TO STOP RUNNING LABS
            elif output ==1:
                return 'Lab Verification Error'
    elif opt == 'Create a new custom Lab':
        lab_option = st.selectbox(
        'What Type of lab would you like to create?', ('Routing', 'Switching', 'Topology Map'))
        return opt
    elif opt == 'Other':
        return opt
    else:
        return 'Please Select one Option'




st.write('You have selected:', take_action(option))

if st.button('Display Running Labs'): # FIX CONDITION TO DISPLAY PROPER MESSAGE WHEN NO LABS ARE RUNNING
    disp_run_lab = subprocess.run('containerlab inspect --all', stdout=subprocess.PIPE, text=True, shell=True)
    st.code(disp_run_lab.stdout)
else:
    st.write('No Running Labs')




#user_selection = input('Enter your Oprtion: ')

#def execute_clab_cmd(user_opt):
#    # CLAB run command
#    #cmd_up = 'containerlab deploy -t arista.labtest.yml'
#    #cmd_down = 'containerlab destroy -t arista.labtest.yml --graceful'
#    if user_opt == '1':
#        temp = subprocess.run('containerlab deploy -t arista.labtest.yml', stdout=subprocess.PIPE, text=True, shell=True)
#        output = str(temp.communicate())
#        return output
#    elif user_opt == '2':
#        temp = subprocess.run('containerlab destroy -t arista.labtest.yml --graceful', stdout=subprocess.PIPE, text=True, shell=True)
#        output = str(temp.communicate())
#        return output
#    else:
#        return 'Error or Invalid option'

#print(f'You Selected Option:  {user_selection}')

#execute_clab_cmd(user_selection)






