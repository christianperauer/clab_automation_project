import streamlit as st
import utils
import json
import config
from git import Repo
import os
from pathlib import Path
from tinydb import TinyDB, Query


if "load_state" not in st.session_state:
     st.session_state.load_state = False

def lab_clone():
    labs_parent_dir = config.appRoot + config.labRoot
    repo_dir = ''
    repo_path = Path(labs_parent_dir + repo_dir)
    repo_git = Path(labs_parent_dir + repo_dir + ".git")
    if repo_path.is_dir():
        print("Warning Path already exists, checking for existing git repo")
        if repo_git.is_file():
            print("Git repo already in this directory, delete it before trying again")
        else:
            print(f"Cloning repo from {git_url}")
            Repo.clone_from(git_url, labs_parent_dir + repo_dir)
    else:
        print(f"Making directory {repo_path}")
        os.mkdir(labs_parent_dir + repo_dir)
        print(f"Cloning repo from {git_url}")
        Repo.clone_from(git_url, labs_parent_dir + repo_dir)


def load_page():
    installed_labs, add_lab, update_lab, delete_lab, upload_lab = st.tabs(['Installed Labs', 'Add Lab', 'Update Lab', 'Delete Lab', 'Upload Lab File'])

    with installed_labs:
        st.header('Installed Labs')

        option = st.selectbox(
            'Currently installed labs',
            utils.get_db_labs()
        )

        st.write("Select a lab to view it's details, or use the checkbox below to see all labs")

        all_labs = st.checkbox('Get All Labs')

        if st.button('Get Lab Details'):
            if all_labs == True:
                lab_details = utils.all_lab_details()
            else:
                lab_details = utils.search_lab_details(option)
            
            for lab in lab_details:
                with st.container():
                    lab_table = f"""
                    |  |  |
                    | --- |--- |
                    | **Lab Name** | {lab['name']} |
                    | **Description** | {lab['description']} |
                    | **Author** | {lab['author']} |
                    | **Git Enabled** | {lab['git']} |
                    | **Local Folder** | {lab['localLabFolder']} |
                    | **Lab File** | {lab['labFile']} |
                    | **Git Repo** | {lab['gitRepo']} |
                    """
                    st.markdown(utils.format_md_table(), unsafe_allow_html=True)
                    st.markdown(lab_table)
                    st.write("---")


    with add_lab:
        st.header('Add Lab')

        with st.form("Add New Lab"):

            lab_name = st.text_input('Lab Name')
            lab_shortname = lab_name.lower()
            description = st.text_area('Description')
            author = st.text_input('Author')
            git_enabled = st.checkbox('Use Git Repo?')
            git_url = ''
            if git_enabled:
                git_url = st.text_input('Git URL')
            local_folder = st.text_input('Local Folder')
            lab_file = st.text_input('Lab File Name')
            

            lab_details_json = {
                "name": lab_name,
                "shortname": lab_shortname,
                "author": author,
                "git": git_enabled,
                "localLabFolder": local_folder,
                "labFile": lab_file,
                "gitRepo": git_url,
                "description": description
            }

            submitted = st.form_submit_button("Submit")

            if submitted:
                add_result = utils.db_add_lab(lab_details_json)
                if type(add_result) is int:
                    st.success('Lab Added Successfully', icon="✅")
                elif type(add_result) is Exception:
                    st.error('Lab load failed', icon="🚨")
                else:
                    st.error(f'Did not expect that... result was: {add_result}')

    with update_lab:
        st.write('Update Lab')

    with delete_lab:
        st.write('Delete Lab')

    with upload_lab:
        st.header('Upload Lab File')
        utils.upload_lab()

if __name__ == "__main__":
    load_page()
