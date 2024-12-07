import streamlit as st
import mysql.connector
from datetime import datetime
# Fungsi untuk menghubungkan ke database MySQL
def connect_to_database():
    try:
        return mysql.connector.connect(
            host="robbysaidi.tail78c0a6.ts.net",  # atau IP server MySQL
            port=3306,
            user="root",       
            password="04207027",  
            database="facebase"   
        )
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

