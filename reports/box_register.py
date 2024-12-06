import streamlit as st
from pilih_halaman.login import show_user_attendance, fetch_all_users
import pandas as pd
import mysql.connector
import plotly.express as px

def proces_class():
    st.title("Proses Kelas")

    # Pilihan untuk menampilkan data absensi
    option = st.selectbox(
        "Tampilkan Data Attendance",
        ["Pilih Data", "Data Frame dari show_user_attendance"],
        key="selectbox_options"
    )
    
    if option == "Data Frame dari show_user_attendance":
        attendance_df = show_user_attendance()
        if attendance_df.empty:
            st.write("Tidak ada riwayat absensi yang tercatat.")
        else:
            st.subheader("Data Attendance")
            st.dataframe(attendance_df, use_container_width=True)

    # Pilihan untuk menampilkan data pengguna
    option_2 = st.selectbox(
        "Tampilkan Data Pengguna",
        ["Pilih Data", "Data Frame dari fetch_all_users"],
        key="selectbox_options_2"
    )
    
    if option_2 == "Data Frame dari fetch_all_users":
        users_df = fetch_all_users()
        if users_df.empty:
            st.write("Belum ada data pengguna yang terdaftar.")
        else:
            st.subheader("Data Pengguna Terdaftar")
            st.dataframe(users_df, use_container_width=True)

    # Menampilkan grafik kehadiran
    st.subheader("Grafik Kehadiran Berdasarkan Status dan Alasan")
    attendance_df = show_user_attendance()
    if not attendance_df.empty and "Status" in attendance_df.columns:
        # Grafik Kehadiran vs Ketidakhadiran
        status_summary = attendance_df["Status"].value_counts().reset_index()
        status_summary.columns = ["Status", "Jumlah"]
        
        fig_status = px.bar(
            status_summary, 
            x="Status", 
            y="Jumlah", 
            color="Status",
            title="Jumlah Kehadiran Berdasarkan Status",
            labels={"Status": "Status Kehadiran", "Jumlah": "Jumlah Orang"},
        )
        st.plotly_chart(fig_status, use_container_width=True)

        # Grafik Alasan Ketidakhadiran
        if "Alasan_Ketidakhadiran" in attendance_df.columns:
            reason_summary = attendance_df["Alasan_Ketidakhadiran"].value_counts().reset_index()
            reason_summary.columns = ["Alasan", "Jumlah"]

            fig_reason = px.pie(
                reason_summary, 
                values="Jumlah", 
                names="Alasan", 
                title="Distribusi Alasan Ketidakhadiran",
            )
            st.plotly_chart(fig_reason, use_container_width=True)
    else:
        st.write("Data Kehadiran Tidak Memiliki Informasi Status atau Alasan.")

if __name__ == "__main__":
    proces_class()
