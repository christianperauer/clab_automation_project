import time
import paramiko
import streamlit as st
from utils import get_output, send_cmd

def main():
    
    #Execution starts here.
    
    host_dict = {
        "172.20.20.2":"show ip route", # Feed device names from lab details and add commands from user input
        "172.20.20.3":"show ip route", # asking from a dialogue box - then add to dict values
    }

    with st.form("ssh connection"):
        st.write("Lab Devices")
        option = st.selectbox(
            'Select a Device:', tuple(host_dict.keys())
        )

        submitted = st.form_submit_button("Retrieve Data")
        if submitted:
            #For each host in the inventory dict, extract key and value
            for hostname, cmd in host_dict.items():
                #Paramiko can be SSH client or server; use client here
                conn_params = paramiko.SSHClient()

                #Preventing paramiko to refuse connections due to missing SSH keys
                conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                conn_params.connect(
                    hostname = hostname,
                    port = 22,
                    username = "admin",
                    password = "admin",
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
    main()
