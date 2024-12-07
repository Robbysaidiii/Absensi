
import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import mysql.connector
from FaceBase import connect_to_database
from HOG import compute_hog_features
from pilih_halaman.Daftar import verify_user

def show_user_attendance():
    """
    Menampilkan daftar absensi pengguna.
    """
    pass

def fetch_all_users():
    """
    Mengambil semua data pengguna dari tabel `user` dan absensi terakhir mereka.
    """
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            u.id AS ID, 
            u.nama AS Nama, 
            a.waktu AS Waktu, 
            a.status AS Status, 
            a.alasan_ketidakhadiran AS Alasan
        FROM user u
        LEFT JOIN atendance a 
        ON a.waktu = (
            SELECT MAX(waktu) 
            FROM atendance 
            WHERE user_id = u.id
        ) AND a.user_id = u.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    if results:
        return pd.DataFrame(results)
    else:
        return pd.DataFrame(columns=["ID", "Nama", "Waktu", "Status", "Alasan"])

def validate_user(user_id, user_name):
    """
    Validasi apakah ID dan Nama cocok dalam tabel `user`.
    """
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM user WHERE id = %s AND nama = %s"
    cursor.execute(query, (user_id, user_name))
    result = cursor.fetchone()
    conn.close()
    return result

def save_attendance(user_id, status, reason):
    """
    Simpan data absensi ke dalam tabel `atendance`.
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO atendance (user_id, waktu, status, alasan_ketidakhadiran) VALUES (%s, %s, %s, %s)",
            (user_id, datetime.now(), status, reason if reason else None)
        )
        conn.commit()
        st.success("Data absensi berhasil disimpan.")
    except mysql.connector.Error as err:
        st.error(f"Gagal menyimpan absensi: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def attendance_page():
    """
    Halaman utama untuk absensi.
    """
    st.title("Halaman Absensi")

    # Input data pengguna
    st.subheader("Masukkan Data Anda")
    user_id = st.text_input("ID")
    user_name = st.text_input("Nama")
    user_note = st.text_area("Keterangan (Opsional)")

    if st.button("Lanjutkan Verifikasi Wajah"):
        if not user_id or not user_name:
            st.warning("Harap isi ID dan Nama terlebih dahulu.")
        else:
            # Validasi ID dan Nama
            user_info = validate_user(user_id, user_name)
            if user_info:
                st.write("Gunakan kamera untuk mengambil foto wajah.")
                picture = st.camera_input("Ambil Foto untuk Verifikasi")
                if picture:
                    # Decode gambar dari input kamera
                    image_bytes = picture.getvalue()
                    frame = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                    
                    # Ekstraksi fitur HOG dari gambar
                    hog_features = compute_hog_features(frame)
                    
                    # Verifikasi wajah dengan data yang ada
                    verification_result = verify_user(hog_features)

                    if verification_result == user_info['id']:
                        st.success(f"Verifikasi wajah berhasil untuk {user_name}!")

                        # Tombol untuk menyimpan absensi setelah verifikasi wajah
                        if st.button("Absen"):
                            # Simpan absensi ke database
                            with st.spinner("Menyimpan data absensi..."):
                                save_attendance(user_id, "Hadir", user_note)
                            st.success(f"Absensi berhasil dicatat:\n- **Nama:** {user_name}\n- **ID:** {user_id}")
                            # Refresh tabel setelah absen
                            st.experimental_rerun()
                    else:
                        st.error("Verifikasi wajah gagal! Pastikan wajah Anda terlihat jelas.")
            else:
                st.error("ID dan Nama tidak ditemukan! Silakan lakukan pendaftaran terlebih dahulu.")

# Tampilkan semua pengguna dan absensi terakhir
    st.subheader("Daftar Pengguna dan Riwayat Absensi Terakhir")
    user_data = fetch_all_users()
    if not user_data.empty:
        # Tabel dengan lebar container penuh dan tinggi yang dapat disesuaikan
        st.dataframe(user_data, use_container_width=True, height=600)
    else:
        st.write("Tidak ada data pengguna yang ditemukan.")
if __name__ == "__main__":
    attendance_page()
