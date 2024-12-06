import streamlit as st
import mysql.connector
import numpy as np
from datetime import datetime
import time
import cv2
from HOG import compute_hog_features  

# Fungsi untuk menghubungkan ke database MySQL
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="facebase"
    )

def fetch_attendance_data(selected_class):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)

    # Ambil data absensi dari database berdasarkan kelas
    query = """
       SELECT 
    a.user_id AS ID,
    u.nama AS Nama,
    a.status AS Kehadiran,
    a.waktu AS Jam,
    a.alasan AS Keterangan
FROM attendance a
JOIN user u ON a.user_id = u.id
WHERE u.kelas = %s
ORDER BY a.waktu DESC

    """
    cursor.execute(query, (selected_class,))
    results = cursor.fetchall()

    conn.close()

    # Jika tidak ada data, kembalikan DataFrame kosong
    if not results:
        return pd.DataFrame(columns=["ID", "Nama", "Kehadiran", "Jam", "Keterangan"])

    # Konversi hasil query menjadi DataFrame
    return pd.DataFrame(results)

# Fungsi untuk mendaftarkan pengguna baru
def register_new_user(user_id, name, age, address, college, hog_features):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Menyimpan data pengguna dan fitur HOG-nya dalam bentuk byte
    cursor.execute("INSERT INTO user (id, nama, umur, alamat, kuliah, hog_features) VALUES (%s, %s, %s, %s, %s, %s)",
                   (user_id, name, age, address, college, hog_features.tobytes()))  # Simpan sebagai bytes
    conn.commit()
    cursor.close()
    conn.close()
    return "Registrasi berhasil!"

# Fungsi untuk menyimpan absensi
def save_attendance(user_id, status, alasan=None):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Menyimpan absensi dengan waktu saat ini
    waktu_absen = datetime.now()  # Waktu saat ini
    cursor.execute("INSERT INTO attendance (user_id, waktu, status, alasan) VALUES (%s, %s, %s, %s)",
                   (user_id, waktu_absen, status, alasan))
    conn.commit()
    cursor.close()
    conn.close()
    return "Absensi berhasil dicatat!"

# Fungsi untuk menampilkan absensi pengguna
def show_user_attendance(user_info):
    st.write(f"Menampilkan absensi untuk {user_info['nama']} ({user_info['id']})")

    conn = connect_to_database()
    cursor = conn.cursor()

    # Ambil absensi pengguna berdasarkan ID
    cursor.execute("SELECT waktu, status, alasan FROM attendance WHERE user_id = %s ORDER BY waktu DESC", (user_info['id'],))
    results = cursor.fetchall()

    if len(results) == 0:
        st.write("Tidak ada absensi yang tercatat.")
    else:
        for row in results:
            waktu, status, alasan = row
            st.write(f"Waktu: {waktu}, Status: {status}, Alasan: {alasan if alasan else 'Tidak ada'}")
    
    cursor.close()
    conn.close()

def show_registered_users():
    st.title("Informasi Pengguna Terdaftar")

    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil data dari tabel `user` untuk pengguna yang sudah terdaftar
    cursor.execute("SELECT id, nama, umur, alamat, kuliah FROM user")
    results = cursor.fetchall()
    
    if len(results) == 0:
        st.write("Belum ada pengguna yang terdaftar.")
    else:
        # Konversi hasil query ke DataFrame
        df = pd.DataFrame(results)
        st.write("Berikut adalah daftar pengguna yang sudah terdaftar:")
        st.table(df)  # Tampilkan data dalam bentuk tabel
    
    cursor.close()
    conn.close()
# Fungsi untuk memverifikasi wajah dan mendapatkan data pengguna
def verify_user(hog_features):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nama, umur, alamat, kuliah, hog_features FROM user")
    results = cursor.fetchall()
    
    for row in results:
        user_id, name, age, address, college, stored_hog_features = row
        stored_hog_features = np.frombuffer(stored_hog_features, dtype=np.float64)  # Memastikan dtype sesuai
        
        # Hitung jarak antara fitur HOG login dan fitur yang disimpan
        distance = np.linalg.norm(hog_features - stored_hog_features)
        
        if distance < 10:  # Misalnya threshold 10
            return user_id, name, age, address, college  # Kembalikan informasi pengguna

    return 'unknown_person'
# Fungsi untuk mendaftarkan pengguna baru
def register_user():
    st.title("Registrasi Pengguna Baru")
    
    # Input untuk data pengguna
    name = st.text_input("Nama")
    age = st.number_input("Umur", min_value=1, max_value=100)
    address = st.text_area("Alamat")
    college = st.text_input("Kuliah")
    
    # Ambil gambar dari webcam
    picture = st.camera_input("Ambil Foto untuk Pendaftaran")
    
    if picture:
        image_bytes = picture.getvalue()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Menghitung fitur HOG
        hog_features = compute_hog_features(frame)
        
        # ID unik untuk pengguna baru
        user_id = np.random.randint(1000, 9999)
        
        # Mendaftarkan pengguna baru
        response = register_new_user(user_id, name, age, address, college, hog_features)
        st.success(response)

# Fungsi untuk mencatat absensi
def mark_attendance(user_info):
    st.write(f"Absensi untuk {user_info['nama']} ({user_info['id']})")

    # Pilih status kehadiran
    status = st.selectbox("Status Kehadiran", ["Hadir", "Tidak Hadir"])

    # Jika tidak hadir, beri alasan
    alasan = None
    if status == "Tidak Hadir":
        alasan = st.text_area("Alasan Ketidakhadiran", "")
    
    if st.button("Simpan Absensi"):
        # Simpan absensi ke database
        response = save_attendance(user_info["id"], status, alasan)
        st.success(response)


# Halaman Login dan Verifikasi Wajah
def show_login():
    st.title("Halaman Login")
    st.write("Silakan pilih metode input gambar.")

    # Pilih metode input gambar
    upload_option = st.selectbox("Pilih metode input gambar", ("Unggah Gambar", "Webcam", "Registrasi Pengguna Baru"))
    
    if upload_option == "Registrasi Pengguna Baru":
        register_user()

    elif upload_option == "Unggah Gambar":
        uploaded_image = st.file_uploader("Unggah Gambar", type=["jpg", "png", "jpeg"])
        if uploaded_image:
            image_bytes = uploaded_image.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Menghitung fitur HOG
            hog_features = compute_hog_features(frame)
            user_info = verify_user(hog_features)
            
            if user_info != "unknown_person":
                st.success(f"Wajah {user_info['nama']} dikenali!")
                mark_attendance(user_info)
                show_user_attendance(user_info)
            else:
                st.error("Wajah tidak dikenali!")

    elif upload_option == "Webcam":
        picture = st.camera_input("Ambil foto menggunakan webcam")
        if picture:
            image_bytes = picture.getvalue()
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Menghitung fitur HOG
            hog_features = compute_hog_features(frame)
            user_info = verify_user(hog_features)
            
            if user_info != "unknown_person":
                st.success(f"Wajah {user_info['nama']} dikenali!")
                mark_attendance(user_info)
                show_user_attendance(user_info)
            else:
                st.error("Wajah tidak dikenali!")

if __name__ == "__main__":
    show_login()
 

