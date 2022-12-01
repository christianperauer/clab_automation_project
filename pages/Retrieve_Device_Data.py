import paramiko
import streamlit as st
from utils import get_output, send_cmd

def main():
    """
    Execution starts here.
    """
    host_dict = {
        "172.20.20.2":"show ip route",
        "172.20.20.3":"show ip route",
    }

    with st.form("ssh connection"):
        st.write("Lab Devices")
        option = st.selectbox(
            'Select a Device:', tuple(host_dict.keys())
        )



    #For each host in the inventory dict, extract key and value
    for hostname, cmd in host_dict.items():
        #Paramiko can be SSH client or server; use client here
        conn_params = paramiko.SSHClient()

        #We don't need paramiko to refuse connections due to missing SSH keys
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
        print(f"Logged into {get_output(conn).strip()} sucessfully")

        commands = [
            cmd,
        ]
        for command in commands:
            send_cmd(conn,command)
            print(get_output(conn))

        #Close session when we are done
        conn.close()

if __name__ == "__main__":
    main()
