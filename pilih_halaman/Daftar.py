import streamlit as st
import cv2
import mysql.connector
import numpy as np
import time
import pandas as pd  # Import pandas untuk menampilkan dataframe
from FaceBase import connect_to_database
from HOG import compute_hog_features

# Fungsi untuk mendaftarkan pengguna baru ke database
def register_new_user(name, age, address, college, hog_features):
    """
    Fungsi untuk mendaftarkan pengguna baru ke database.
    Menggunakan AUTO_INCREMENT untuk user_id.
    """
    if hog_features is None:
        return "Gagal memproses gambar. Fitur HOG tidak dapat dihitung."

    conn = connect_to_database()
    if conn is None:
        return "Database connection failed!"

    cursor = conn.cursor()

    try:
        # Menyimpan fitur HOG dalam bentuk BLOB (bytes)
        cursor.execute("INSERT INTO user (nama, umur, alamat, kuliah, hog_features) VALUES (%s, %s, %s, %s, %s)",
                       (name, age, address, college, hog_features.tobytes()))  # Simpan fitur HOG sebagai bytes
        conn.commit()
        cursor.close()
        conn.close()
        return "Registrasi berhasil!"
    except mysql.connector.Error as err:
        conn.rollback()
        conn.close()
        return f"Error saat registrasi: {err}"

# Fungsi untuk memverifikasi pengguna berdasarkan fitur HOG
def verify_user(hog_features):
    """
    Fungsi untuk memverifikasi pengguna berdasarkan fitur HOG.
    """
    conn = connect_to_database()
    if conn is None:
        return 'unknown_person'

    cursor = conn.cursor()
    cursor.execute("SELECT id, nama, umur, alamat, kuliah, hog_features FROM user")
    results = cursor.fetchall()

    for row in results:
        user_id, name, age, address, college, stored_hog_features = row

        if stored_hog_features is None:
            # Abaikan baris dengan hog_features kosong
            continue
        
        # Mengonversi BLOB kembali ke fitur HOG
        stored_hog_features = np.frombuffer(stored_hog_features, dtype=np.float64)

        # Hitung jarak antara fitur HOG login dan fitur yang disimpan
        distance = np.linalg.norm(hog_features - stored_hog_features)

        if distance < 10:  # Misalnya threshold 10
            return {"id": user_id, "nama": name, "umur": age, "alamat": address, "kuliah": college}

    return 'unknown_person'

# Fungsi untuk menampilkan daftar pengguna yang terdaftar dalam bentuk dataframe
def display_users():
    """
    Menampilkan data pengguna yang sudah terdaftar dalam bentuk tabel.
    """
    conn = connect_to_database()
    if conn is None:
        st.error("Gagal menghubungkan ke database.")
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama, umur, alamat, kuliah FROM user")
    results = cursor.fetchall()

    # Menyusun hasil query menjadi dataframe pandas
    df = pd.DataFrame(results, columns=["ID", "Nama", "Umur", "Alamat", "Kuliah"])
    
    # Menampilkan dataframe di Streamlit
    st.dataframe(df)

    cursor.close()
    conn.close()

# Fungsi untuk halaman pendaftaran pengguna baru di Streamlit
def show_register():
    """
    Halaman pendaftaran pengguna baru di Streamlit.
    """
    st.title("Halaman Register")
    st.write("Silakan isi form untuk mendaftar.")

    # Input data pengguna
    user_id = st.text_input("ID Pengguna", key="register_user_id")
    name = st.text_input("Nama", key="register_name")
    age = st.number_input("Umur", min_value=0, key="register_age")
    address = st.text_input("Alamat", key="register_address")
    college = st.text_input("Kuliah", key="register_college")

    # Pilihan metode input gambar
    upload = st.radio("Pilih metode input gambar:", ("Upload", "Webcam"))

    frame = None  # Tempat menyimpan gambar

    # Upload gambar
    if upload == "Upload":
        uploaded_image = st.file_uploader("Unggah Gambar", type=['jpg', 'png', 'jpeg'], key="upload_image")  # Added unique key
        if uploaded_image:
            st.image(uploaded_image, caption="Gambar yang diunggah", use_container_width=True)
            image_bytes = uploaded_image.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Input gambar dari webcam
    elif upload == "Webcam":
        picture = st.camera_input("Gunakan webcam untuk mengambil gambar", key="webcam_image")  # Added unique key
        if picture:
            st.image(picture, caption="Gambar dari webcam", use_container_width=True)
            image_bytes = picture.getvalue()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Tombol untuk melakukan pendaftaran
    if st.button("Daftar"):
        # Validasi input
        if not (name and age and address and college):
            st.error("Semua kolom harus diisi!")
        elif frame is None:
            st.error("Harap ambil gambar menggunakan kamera atau unggah gambar!")
        else:
            # Menampilkan progress bar
            progress_text = "Proses pendaftaran sedang berjalan. Mohon tunggu."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(0, 100, 10):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 10, text=progress_text)

            # Proses pendaftaran
            hog_features = compute_hog_features(frame)
            user_info = verify_user(hog_features)
            if user_info != 'unknown_person':
                st.error("ID dan wajah sudah terdaftar! Silakan gunakan ID yang berbeda.")
            else:
                result = register_new_user(name, age, address, college, hog_features)
                st.success(result)

            # Menghapus progress bar setelah selesai
            time.sleep(1)
            my_bar.empty()

    # Menampilkan daftar pengguna yang terdaftar
    st.subheader(" Pengguna Terdaftar")
    display_users()

# Jalankan halaman pendaftaran
if __name__ == "__main__":
    show_register()
