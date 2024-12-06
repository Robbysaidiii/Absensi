import cv2
import numpy as np
import pandas as pd
import streamlit as st
from halaman import show_home
from pilih_halaman.Daftar import show_register
from pilih_halaman.login import attendance_page
from streamlit_option_menu import option_menu
from reports.alerts import process_class
from reports.box_register import proces_class
import time

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("Navigation")
    selected_page = option_menu(
        menu_title="Main Menu",
        options=["Home", "Register", "Absen", "Agree", "Proces Class"],
        icons=["house", "person", "key", "check-circle", "clipboard"],
        menu_icon="cast",
        default_index=0
    )

# Main Content Based on Sidebar Selection
if selected_page == "Home":
    show_home()

elif selected_page == "Register":
    show_register()

elif selected_page == "Absen":
    attendance_page()

elif selected_page == "Agree":
    proces_class()
elif selected_page == "Proces Class":
    process_class()
# Optional: Add Spinner for Initial Load
with st.sidebar:
    with st.spinner("Loading sidebar..."):
        time.sleep(1)
    st.success("berhasil diakses")
