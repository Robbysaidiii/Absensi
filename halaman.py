import streamlit as st

def show_home():
    st.title("Face Recognition Histogram of Oriented Gradient")

    st.markdown(
        """
        Aplikasi ini menggunakan metode Histogram of Oriented Gradients (HOG) untuk mengenali wajah. HOG adalah teknik pengolahan citra yang sangat efektif untuk mendeteksi objek, terutama wajah, dengan memanfaatkan fitur-fitur orientasi dari gradient intensitas pada gambar.

       ### Pendahuluan

        Kegiatan perkuliahan tidak terlepas dari proses absensi yang merupakan bagian penting dalam mencatat kehadiran mahasiswa. Absensi yang akurat sangat diperlukan untuk memastikan mahasiswa hadir dalam setiap sesi kuliah, serta untuk mendukung pengelolaan akademik yang lebih baik. Namun, metode absensi konvensional seperti daftar hadir manual sering kali menimbulkan berbagai kendala, seperti kecurangan, keterlambatan, dan kesulitan dalam pengolahan data kehadiran.

        Untuk mengatasi masalah tersebut, aplikasi "Face Recognition Histogram of Oriented Gradient" hadir sebagai solusi inovatif. Dengan memanfaatkan teknologi pengenalan wajah, aplikasi ini memungkinkan proses absensi dilakukan secara otomatis dan efisien. Melalui pengenalan wajah yang akurat, aplikasi ini tidak hanya meningkatkan keandalan data kehadiran tetapi juga memberikan kemudahan bagi mahasiswa dan pengajar dalam melakukan pencatatan kehadiran.

        
       ### AI Project Cycle

        1. **Problem Scoping**: Mengembangkan sistem pengenalan wajah untuk absensi otomatis guna meningkatkan efisiensi dan akurasi kehadiran mahasiswa.
   
        2. **Data Acquisition**: gambar wajah setiap mahasiswa di ambil secara manual menggunakan webcam dan mengisi informasi profil melalui formulir Register.

        3. **Data Exploration**: menggunakan webcam untuk mengambil gambar pada area wajah untuk membantu mengidentifikasi objek.

        4. **Modeling**: Menggunakan Histogram of Oriented Gradient untuk ekstraksi fitur dan menerapkan algoritma klasifikasi KNN untuk pengenalan wajah.

        5. **Evaluasi**: Di uji pada 5 wajah yang berbeda dan model dengan tepat mencocokkan wajah. Model mengukur akurasi dengan metrik seperti precision.

        6. **Deployment**: Membangun aplikasi web menggunakan Streamlit, OpenCV, NumPy, scikit-image, dan MySQL Connector.
    
         ### Cara Kerja Aplikasi:
        1. **Registrasi**: Pengguna mendaftar dengan mengambil foto wajah.
        2. **Login**: Pengguna melakukan login dengan memverifikasi wajah mereka.
        3. **Absensi Otomatis**: Kehadiran dicatat berdasarkan verifikasi wajah.
        4. **Data dan Visualisasi**: Menampilkan data pengguna dan kehadiran.
       """,
        unsafe_allow_html=True
    )

    # Graphviz Diagram
    st.subheader("Cara Kerja - Diagram Alur")
    st.graphviz_chart(
        """
       digraph G {
        rankdir=LR;
        node [shape=box, style=filled, color=lightblue];
        "Mulai" -> "Registrasi Wajah" [label="Input Data"];
        "Registrasi Wajah" -> "Verifikasi Wajah" [label="Login"];
        "Verifikasi Wajah" -> "Absensi Otomatis" [label="Pencocokan Data"];
        "Absensi Otomatis" -> "Simpan Kehadiran" [label="Ke Database"];
        "Simpan Kehadiran" -> "Tampilkan Data & Statistik" [label="Output"];
        "Tampilkan Data & Statistik" -> "Selesai";
    }
        """
    )
    st.graphviz_chart('''
        digraph {
            "Mulai" -> "Registrasi Wajah"
            "Registrasi Wajah" -> "Verifikasi Wajah"
            "Verifikasi Wajah" -> "Absensi Otomatis"
            "Absensi Otomatis" -> "Simpan Kehadiran"
            "Simpan Kehadiran" -> "Tampilkan Data & Statistik"
            "Tampilkan Data & Statistik" -> "Selesai"
        }
    ''')

if __name__ == "__main__":
    show_home()
