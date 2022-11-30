import streamlit as st
from utils import load_lab, check_run, destroy_lab

def load_page():

    with st.form("load lab"):
        st.write("Lab loading form")
        option = st.selectbox(
            'Select a lab:', ('', 'Arista', 'Cumulus', 'CSR')
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner(text="Checking if lab is already running"):
                lab_check = check_run(option)
            if lab_check.returncode == 0 and lab_check.stdout == '':
                with st.spinner(text="Lab loading..."):
                    lab = load_lab(option)
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
                    st.code(lab_check.stdout)
            elif lab_check.returncode == 1:
                st.error('Error checking if lab is running', icon="🚨")

if __name__ == "__main__":
    load_page()
