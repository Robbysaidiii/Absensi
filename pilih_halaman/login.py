import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
from FaceBase import verify_user, save_attendance, show_login, connect_to_database
from HOG import compute_hog_features

def show_user_attendance():
    """
    Menampilkan riwayat absensi untuk pengguna berdasarkan ID dalam bentuk DataFrame.
    """
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query ="SELECT attendance_id AS attendance_id ,user_id AS user_id,waktu AS waktu,Status AS Status,Alasan_Ketidakhadiran AS Alasan_Ketidakhadiran FROM attendance"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    # Konversi hasil query ke DataFrame
    if results:
        return pd.DataFrame(results)
    else:
        return pd.DataFrame(columns=["attendance_id", "user_id", "waktu", "Status", "Kuliah","Alasan_Ketidakhadiran"])

def fetch_all_users():
    """
    Mengambil semua data pengguna dari tabel `user` dan data absensi terkait.
    """
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    # Query untuk mengambil data pengguna dengan data absensi terakhir
    query = """
        SELECT 
            u.id AS ID, 
            u.nama AS Nama, 
            u.umur AS Umur, 
            u.alamat AS Alamat, 
            u.kuliah AS Kuliah,
            a.waktu AS Waktu, 
            a.status AS Status, 
            a. Alasan_Ketidakhadiran AS Alasan_Ketidakhadiran
        FROM user u
        LEFT JOIN (
            SELECT user_id, MAX(waktu) AS waktu, status, Alasan_Ketidakhadiran
            FROM attendance 
            GROUP BY user_id
        ) a ON u.id = a.user_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    # Konversi hasil query ke DataFrame
    if results:
        return pd.DataFrame(results)
    else:
        return pd.DataFrame(columns=["ID", "Nama", "Umur", "Alamat", "Kuliah", "Waktu", "Status", "Alasan_Ketidakhadiran"])

# Fungsi utama untuk absensi
def attendance_page():
    st.title("Halaman Absensi")

    # Pilihan kelas
    selected_class = st.selectbox(
        "Pilih Kelas",
        ["K1 Awanpintar", "K2 Sapiens", "K3 Cosmic", "K4 Apollo", "K5 Photon", "K6 Turing"]
    )
    st.write(f"**Kelas yang dipilih:** {selected_class}")

    # Input untuk ID, Nama, dan Keterangan
    st.subheader("Masukkan Data Anda")
    user_id = st.text_input("ID")
    user_name = st.text_input("Nama")
    user_note = st.text_area("Keterangan (Opsional)")

    # Jika data sudah diisi, perintahkan untuk verifikasi wajah
    if st.button("Lanjutkan Verifikasi Wajah"):
        if not user_id or not user_name:
            st.warning("Harap isi ID dan Nama terlebih dahulu.")
        else:
            st.write("Gunakan kamera untuk verifikasi wajah.")
            picture = st.camera_input("Ambil Foto untuk Verifikasi")
            if picture:
                # Proses verifikasi wajah
                image_bytes = picture.getvalue()
                frame = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                hog_features = compute_hog_features(frame)
                user_info = verify_user(hog_features)

                if user_info != "unknown_person":
                    st.success(f"Wajah {user_name} berhasil diverifikasi!")
                    
                    # Simpan absensi ke database
                    current_time = datetime.now().strftime("%H:%M:%S")
                    save_attendance(user_id, "Hadir", user_note)
                    
                    st.write(f"Absensi Anda berhasil dicatat:")
                    st.write(f"- **Nama:** {user_name}")
                    st.write(f"- **ID:** {user_id}")
                    st.write(f"- **Keterangan:** {user_note or 'Tidak ada'}")
                    st.write(f"- **Jam Kehadiran:** {current_time}")
                else:
                    st.error("Verifikasi wajah gagal! Pastikan wajah Anda jelas di kamera.")

    # Tampilkan semua data pengguna dalam DataFrame
    st.subheader("Data Pengguna Terdaftar")
    
    users_df = fetch_all_users()
    if users_df.empty:
        st.write("Belum ada data pengguna yang terdaftar.")
    else:
        st.dataframe(users_df)

    st.subheader("DATA KEHADIRAN")
    usersdf = show_user_attendance()
    if usersdf.empty:
        st.write("BELOM ADA DATA ABSEN YANG DIINPUT")
    else:
        st.dataframe(usersdf)
# Jalankan fungsi halaman absensi
if __name__ == "__main__":
    attendance_page()
