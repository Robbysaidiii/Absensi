import streamlit as st
import cv2
import numpy as np
import time
from HOG import compute_hog_features
from FaceBase import verify_user, register_new_user

def show_register():
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
            st.image(uploaded_image, caption="Gambar yang diunggah", use_column_width=True)
            image_bytes = uploaded_image.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Input gambar dari webcam
    elif upload == "Webcam":
        picture = st.camera_input("Gunakan webcam untuk mengambil gambar", key="webcam_image")  # Added unique key
        if picture:
            st.image(picture, caption="Gambar dari webcam", use_column_width=True)
            image_bytes = picture.getvalue()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Tombol untuk melakukan pendaftaran
    if st.button("Daftar"):
        # Validasi input
        if not (user_id and name and age and address and college):
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
                result = register_new_user(user_id, name, age, address, college, hog_features)
                st.success(result)

            # Menghapus progress bar setelah selesai
            time.sleep(1)
            my_bar.empty()
