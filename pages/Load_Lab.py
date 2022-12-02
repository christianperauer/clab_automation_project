import streamlit as st
import streamlit as st
import utils
import json
import config
from git import Repo
import os
from pathlib import Path
from tinydb import TinyDB, Query

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
    labs_list = utils.get_db_labs()
    with st.form("load lab"):
        st.write("Lab loading form")
        option = st.selectbox(
            'Select a lab:', labs_list
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner(text="Checking if lab is already running"):
                lab_check = utils.clab_function("inspect", option)
            if lab_check is None:
                st.write("Lab does not exist, you shouldn't see this")
            elif lab_check is str:
                st.write("Returned message:")
                st.text(lab_check)
            elif lab_check.returncode == 0 and lab_check.stdout == '':
                with st.spinner(text="Lab loading..."):
                    lab = utils.clab_function("deploy", option)
                st.success("Complete")
                if lab.returncode == 0:
                    st.success('Lab loaded successfully!', icon="✅")
                    with st.expander("Lab load details"):
                        st.code(lab.stdout)
                    st.subheader("Logs")
                    with st.expander("Lab load logs"):
                        st.text(lab.stderr)
                elif lab.returncode == 1:
                    st.error("There was a problem loading the lab")

                    with st.expander("Lab load logs"):
                        st.text(lab.stderr)
            elif lab_check.returncode == 0 and lab_check.stdout is not None:
                st.warning('Lab is already running', icon="⚠️")
                with st.expander("Running lab details"):
                    st.code(utils.clab_function("inspect", option).stdout)
            elif lab_check.returncode == 1:
                st.error('Error checking if lab is running', icon="🚨")



if __name__ == "__main__":
    load_page()
