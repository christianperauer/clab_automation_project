import streamlit as st
import utils
from tinydb import TinyDB, Query
import re
import os
from selenium import webdriver
import multiprocessing
import subprocess


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

    st.write("---")

    with st.form("Map Lab Topology"):
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

        st.write("Select Lab Topology to Map")
        option = st.selectbox(
            'Select a lab:', dest_final_list
        )

        map_lab = st.form_submit_button("Map Topology")
        if map_lab:
            with st.spinner(text="Checking Topology Map... Please wait"):                
                target_command = utils.clab_function_map(option)
                # st.write([(target_command)],)

                lab_topo_map = multiprocessing.Process(target=utils.clab_function_run_command, args=([(target_command)],))
                lab_topo_map.start()
                
                with st.expander("Lab Topology Map"):

                    link_text = "Lab " + option + " map"
                    click_url = "http://10.10.0.12:50080/"
                    markdown_link = "[{}]({})".format(link_text, click_url)
                    st.markdown(markdown_link, unsafe_allow_html=True)
                    st.success("Completed, if spinner does not stop, click Stop on the top right hand corner")

                lab_topo_map.join()

    st.write("---")

    with st.form("Terminate Map Function Session"):
        st.write("Terminate Map Function Sessions")
        st.error('NOTE: This feature is a WIP - If button grayed out, click stop on the top right hand corner', icon="⚠️")

        kill_topo_but = st.form_submit_button("Terminate Map Session")
        if kill_topo_but:
            map_pid = utils.clab_function_kill_graph()
            # st.write(map_pid)
            # st.write(type(map_pid))
            subprocess.run(['sudo', 'kill', map_pid], check=True)
            st.success("Completed")

    st.write("---")

if __name__ == "__main__":
    load_page()