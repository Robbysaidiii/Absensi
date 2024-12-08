import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Fungsi untuk menghubungkan ke database MySQL
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="robbysaidi-1.tail78c0a6.ts.net",  # Hostname atau IP server MySQL
            port=3306,                           # Port MySQL
            user="root",                         # Username MySQL
            password="04207027",                 # Password MySQL
            database="facebase"                  # Nama database MySQL
        )
        if conn.is_connected():
            st.success("Berhasil terhubung ke database!")
            return conn
    except Error as err:
        st.error(f"Kesalahan koneksi database: {err}")
        return None

# Fungsi untuk mengambil data pengguna
def fetch_all_users():
    conn = connect_to_database()
    if conn is None:
        st.error("Tidak dapat terhubung ke database. Cek koneksi Anda.")
        return pd.DataFrame(columns=["ID", "Nama", "Waktu", "Status", "Alasan"])
    
    try:
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
            st.write("Tidak ada data absensi untuk pengguna.")
            return pd.DataFrame(columns=["ID", "Nama", "Waktu", "Status", "Alasan"])
    except Error as e:
        st.error(f"Kesalahan saat menjalankan query: {e}")
        return pd.DataFrame(columns=["ID", "Nama", "Waktu", "Status", "Alasan"])

# Fungsi utama
def main():
    st.title("Tes Koneksi Database")
    
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            st.write(f"Terhubung ke database: {db_name['DATABASE()']}")
            cursor.close()
        except Error as e:
            st.error(f"Kesalahan saat menjalankan query: {e}")
        finally:
            conn.close()
            st.info("Koneksi telah ditutup.")
    else:
        st.error("Koneksi ke database gagal.")

if __name__ == "__main__":
    main()
