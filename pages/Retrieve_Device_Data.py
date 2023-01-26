import time
import paramiko
import streamlit as st
from utils import get_output, send_cmd
import utils
import config

if "load_state" not in st.session_state:
     st.session_state.load_state = False

def load_page():
    
    st.header('Retrieve Device Data')

    if st.button('Refresh Currently Running Labs') or st.session_state.load_state:
        st.session_state.load_state = True
        running_labs = utils.get_running_labs()
        lab_list = []
        lab_dev_list = []
        dev_ip_list = []

        if running_labs is None:
            st.error('There are no Labs running', icon="⚠️")
        
        elif running_labs is not None:
            
            for lab in running_labs['containers']:
                if lab['lab_name'] not in lab_list:
                    lab_list.append(lab['lab_name'])

            st.subheader("Currently Running Labs")
            
            for lab_name in lab_list:
                with st.container():
                    lab_desc = f"""
                    #### Lab Name: {lab_name}
                    #### Lab File: 
                    """
                    st.markdown(lab_desc)
                    button_name = f"List {lab_name} Devices"
                    if st.button(button_name):
                        expander_name = f"{lab_name} Devices"
                        with st.expander(expander_name):
                            for container in running_labs['containers']:
                                if container['lab_name'] == lab_name:
                                    container_table = f"""
                                    |  |  |
                                    | --- |--- |
                                    | **Name** | {container['name']} |
                                    | **IPv4 Address** | {container['ipv4_address']} |
                                    """
                                    st.markdown(utils.format_md_table(), unsafe_allow_html=True)
                                    st.markdown(container_table, unsafe_allow_html=True)
                    st.write("---")

    # Device Data Retrieval Execution starts here.

    # Define empty lists to add lab hosts and command combinations
    host_list = []
    host_cmd = []
    host_dict = {}

    with st.form("ssh connection"):
        st.write("Retrieve Data From Devices")

        # Request user to enter the deviec and command to retrieve
        ret_from_dev = st.text_input('Enter Device IP')
        ret_cmd_dev = st.text_input('Enter CLI Command')

        submitted = st.form_submit_button("Retrieve Data")
        if submitted:

            # When clicking the submit button, 
            # the IP address and command are appended to the corresponding lists
            host_list.append(ret_from_dev)
            host_cmd.append(ret_cmd_dev)

            # Zip the populated lists into a dictionary
            if ret_from_dev == "" or ret_cmd_dev == "":
                st.error('Please Enter an IP and a Command', icon="⚠️")
            elif ret_from_dev != "" and ret_cmd_dev != "":
                host_dict = dict(zip(host_list, host_cmd))

            #For each host in the inventory dict, extract key and value
            for hostname, cmd in host_dict.items():
                #Paramiko can be SSH client or server; use client here
                conn_params = paramiko.SSHClient()

                #Preventing paramiko to refuse connections due to missing SSH keys
                conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                conn_params.connect(
                    hostname = hostname,
                    port = config.device_ssh_port,
                    username = config.arista_cred_user,
                    password = config.arista_cred_pass,
                    look_for_keys = False,
                    allow_agent = False,
                )

                #Get an interactive shell and wait a bit for the prompt to appear
                conn = conn_params.invoke_shell()
                time.sleep(1.0)

                st.write(f"Logged into {get_output(conn).strip()} sucessfully")

                commands = [
                    cmd,
                ]
                #Loop through command list to collect from devices
                for command in commands:
                    with st.spinner(text=f"Collecting {command} from {hostname}"):
                        #Send the command upon established connection
                        send_cmd(conn,command)
                        #Capture function return value - command output
                        return_check = get_output(conn)
                        #Load the collected command output into the front end
                        with st.expander("Collected Data"):
                            st.code(return_check)
                            #print(get_output(conn)) - This was an original command of the former script

                #Close session when done
                conn.close()

if __name__ == "__main__":
    load_page()
