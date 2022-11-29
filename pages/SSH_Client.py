import streamlit as st
from utils import connect_to_device

def ssh_to_dev():
    with st.form("ssh connection"):
        st.write("Lab Devices")
        option = st.selectbox(
            'Select a Device:', ('', '172.20.20.2', '172.20.20.3')
        )
        submitted = st.form_submit_button("Connect")
        if submitted:
            with st.spinner(text="Conecting to device %s" % option):
                opt_check = connect_to_device(option)
            if opt_check.stdout is not None:
                # with st.spinner(text="Connecting..."):
                #     ssh_session = connect_to_device(option)
                st.success("Connected!", icon="✅")
                # if ssh_session.returncode == 0:
                #     st.success('Connected via SSH successfully!', icon="✅")
                with st.expander("Connection details"):
                    st.code(opt_check.stdout)
            elif opt_check.stdout is None:
                st.error("There was a problem connecting to the device", icon="🚨")
                with st.expander("Connection logs"):
                    st.text(opt_check.stderr)
            elif opt_check is not None and opt_check.stdout is not None:
                st.warning('Connection already established', icon="⚠️")
                with st.expander("Connection details"):
                    st.code(opt_check.stdout)
            # elif opt_check.returncode == 1:
            #     st.error('Error checking SSH connection', icon="🚨")

if __name__ == "__main__":
    ssh_to_dev()