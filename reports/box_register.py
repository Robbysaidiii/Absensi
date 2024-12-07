import streamlit as st
import pandas as pd
import plotly.express as px
from pilih_halaman.login import fetch_all_users
from pilih_halaman.Daftar import display_users

def proces_class():
    st.title("Proses Kelas")

    # Tampilkan data absensi yang sudah terdaftar
    st.subheader("Data Kehadiran")
    
    # Mengambil data dari fungsi fetch_all_users()
    attendance_df = fetch_all_users()  # Mengambil data untuk digunakan lebih lanjut
    
    if attendance_df.empty:
        st.write("Tidak ada data absensi yang tercatat.")
    else:
        st.dataframe(attendance_df, use_container_width=True)

        # Grafik Distribusi Kehadiran dan Ketidakhadiran
        st.subheader("Grafik Distribusi Kehadiran dan Ketidakhadiran")

        # Gabungkan Status dan Alasan
        if "Status" in attendance_df.columns and "Alasan" in attendance_df.columns:
            # Isi NaN pada alasan dengan 'Tidak Ada Alasan'
            attendance_df["Alasan"] = attendance_df["Alasan"].fillna("Tidak Ada Alasan")
            
            # Gabungkan Status dan Alasan
            attendance_df["Status_Alasan"] = attendance_df["Status"] + " - " + attendance_df["Alasan"]

            # Hitung distribusi gabungan
            combined_summary = attendance_df["Status_Alasan"].value_counts().reset_index()
            combined_summary.columns = ["Status_Alasan", "Jumlah"]

            # Buat pie chart gabungan
            fig_combined = px.pie(
                combined_summary,
                values="Jumlah",
                names="Status_Alasan",
                title="Distribusi Status Kehadiran dan Alasan Ketidakhadiran",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_combined, use_container_width=True)
        else:
            st.write("Data Status atau Alasan tidak ditemukan atau kosong.")

if __name__ == "__main__":
    proces_class()
