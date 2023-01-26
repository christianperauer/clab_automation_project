import streamlit as st
import utils
from tinydb import TinyDB, Query
import re

db = TinyDB("labs.json")
Labs = Query()

if "load_state" not in st.session_state:
     st.session_state.load_state = False

def load_page():
    st.title("Currently Running Labs")
    if st.button('Refresh Currently Running Labs') or st.session_state.load_state:
        st.session_state.load_state = True
        running_labs = utils.get_running_labs()
        lab_list = []

        if running_labs is None:
            st.error('There are no Labs running', icon="⚠️")
        
        elif running_labs is not None:
            
            for lab in running_labs['containers']:
                if lab['lab_name'] not in lab_list:
                    lab_list.append(lab['lab_name'])

            st.subheader("Currently Running Labs")
            
            for lab_name in lab_list:
                #st.write(lab_name)
                with st.container():
                    lab_desc = f"""
                    #### Lab Name: {lab_name}
                    #### Lab File: 
                    """
                    st.markdown(lab_desc)
                    button_name = f"List {lab_name} Containers"
                    if st.button(button_name):
                        expander_name = f"{lab_name} Containers"
                        with st.expander(expander_name):
                            for container in running_labs['containers']:
                                if container['lab_name'] == lab_name:
                                    #st.write(container)
                                    container_table = f"""
                                    |  |  |
                                    | --- |--- |
                                    | **Name** | {container['name']} |
                                    | **Container ID** | {container['container_id']} |
                                    | **Image** | {container['image']} |
                                    | **Kind** | {container['kind']} |
                                    | **State** | {utils.running_lab_status(container['state'])} |
                                    | **IPv4 Address** | {container['ipv4_address']} |
                                    | **IPv6 Address** | {container['ipv6_address']} |
                                    """
                                    st.markdown(utils.format_md_table(), unsafe_allow_html=True)
                                    st.markdown(container_table, unsafe_allow_html=True)
                    st.write("---")
        
    else:
        st.write('Please refresh labs')

    with st.form("Destroy Lab"):
        running_labs = utils.get_running_labs()
        run_labs_list = []
        if running_labs is None:
            st.error('There are no Labs running', icon="⚠️")
        elif running_labs is not None:
            extrLabFromPath = re.compile(r'\S+\/\S+\/(\S+)')
            for lab in running_labs['containers']:
                lab_match_ob = extrLabFromPath.search(lab['labPath'])
                if lab_match_ob.group(1) not in run_labs_list:
                    run_labs_list.append(lab_match_ob.group(1))
                    #st.write(run_labs_list)

        dest_all_labs = db.all()
        dest_lab_list = []
        for lab in dest_all_labs:
            if lab['labFile'] not in dest_lab_list:
                dest_lab_list.append(lab['labFile'])
                #st.write(dest_lab_list)

        dest_final_list = []
        for file in dest_lab_list:
            if file in run_labs_list:
                dest_final_list.append(file)
                #st.write(dest_final_list)

        st.write("Select Lab to Destroy")
        option = st.selectbox(
            'Select a lab:', dest_final_list
        )
        lab_shutdown = st.form_submit_button("Destroy")
        if lab_shutdown:
            with st.spinner(text="Destroy Running Lab... Please wait"):
                lab_destroy = utils.clab_function_des(option)
                st.success("Complete")

if __name__ == "__main__":
    load_page()