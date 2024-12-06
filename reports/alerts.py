import streamlit as st
import streamlit as st
from pilih_halaman.login import show_user_attendance, fetch_all_users
from bokeh.plotting import figure

def process_class():
    st.title("Proses Kelas")

    # Pilihan untuk menampilkan data pengguna
    users_df = fetch_all_users()
    if users_df.empty:
        st.write("Belum ada data pengguna yang terdaftar.")
    else:
        st.subheader("Data Pengguna Terdaftar")
        st.dataframe(users_df, use_container_width=True)

    # Menampilkan grafik perbandingan jumlah orang yang terdaftar dengan target
    st.subheader("Perbandingan Jumlah Orang Terdaftar dengan Target (100 Orang)")

    # Mendapatkan jumlah pengguna
    registered_count = len(users_df)
    target_count = 100

    # Debugging nilai registered_count dan target_count
    st.write("Jumlah Orang Terdaftar:", registered_count)
    st.write("Target Pendaftaran:", target_count)

    # Data untuk grafik
    x = ["Orang Terdaftar", "Sisa Target"]
    y = [registered_count, max(0, target_count - registered_count)]

    # Membuat grafik menggunakan Bokeh
    p = figure(
        title="Perbandingan Pendaftaran", 
        x_axis_label="Kategori", 
        y_axis_label="Jumlah", 
        x_range=x
    )
    p.vbar(x=x, top=y, width=0.6, color=["green", "red"], legend_label="Jumlah")

    # Menampilkan grafik
    st.bokeh_chart(p, use_container_width=True)

if __name__ == "__main__":
    process_class()

