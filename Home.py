import streamlit as st
import config
from tinydb import TinyDB, Query


def load_homepage():
    st.markdown("""
        # NETWORK LAB GENERATOR

        ---

        The very fisrt dynamic Lab generator\n
        The tool provides 2 options:
        * Spin up pre-defined labs
        * Spin up an on demand custom lab
        Supported Vendors so far:
        * Cisco (IOS-XE and IOS-XR)
        * Arista cEOS
        * Nokia SRL
        ---
        
        ##### By ***Terry Fera*** and ***Christian Perauer***

        """)


if __name__ == "__main__":
    load_homepage()