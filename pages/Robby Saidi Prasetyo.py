import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import folium_static
from streamlit_folium import st_folium

# **Memuat CSS Khusus (Opsional)**
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# **Memuat Data Excel**
load_df = pd.read_excel('coordinates.xlsx')  # Data koordinat
load = pd.read_excel('Matakuliah.xlsx')  # Data nilai

# **Membersihkan Data**
if 'Latitude' in load_df.columns:
    load_df['Latitude'] = load_df['Latitude'].apply(lambda x: str(x).replace(',', '.')).astype(float)
if 'Longitude' in load_df.columns:
    load_df['Longitude'] = load_df['Longitude'].apply(lambda x: str(x).replace(',', '.')).astype(float)

valid_df = load_df.dropna(subset=['Latitude', 'Longitude'])

# **Sidebar untuk Filter Data**
name = st.multiselect(
    "Pilih Nama",
    options=valid_df["Name"].unique(),
    default=valid_df["Name"].unique(),
)
df = valid_df.query("Name==@name")

# **Membuat Peta dengan OpenStreetMap (Untuk Debugging)**
m = folium.Map(location=[-6.303818, 106.807566], zoom_start=16)
# **Menambahkan Marker Cluster**
marker_cluster = MarkerCluster().add_to(m)

for i, row in df.iterrows():
    popup_content = f"""
        <h3>Informasi {row['Name']}</h3>
        <ul>
            <li><b>University:</b> {row['University']}</li>
            <li><b>Jenis Kelamin:</b> {row['Jenis kelamin']}</li>
            <li><b>Hobi:</b> {row['Hobi']}</li>
            <li><b>Phone:</b> {row['Phone']}</li>
            <li><b>Gmail:</b> {row['Gmail']}</li>
        </ul>
    """
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        tooltip=row['Name'],
        icon=folium.Icon(color='blue', icon='info-sign'),
    ).add_to(marker_cluster).add_child(folium.Popup(popup_content, max_width=300))

# **Tambahkan HeatMap**
HeatMap([[row['Latitude'], row['Longitude']] for i, row in df.iterrows()]).add_to(m)


with st.expander("Data Student"):
    selected_city = st.selectbox("Select a student", df['Name'])
    selected_row = df[df['Name'] == selected_city].squeeze()
    st.table(selected_row)

# **Menampilkan Peta**
with st.expander("Peta Student Robby "):
    folium_static(m, width=1200, height=600)


# Filter data hanya untuk Robby
robby_data = load[load['Name'] == 'Robby Saidi Prasetyo']
if not robby_data.empty:
    robby_scores = robby_data.iloc[:, 1:]  # Ambil nilai mata kuliah saja
    rata_rata = robby_scores.mean(axis=1).iloc[0]  # Hitung rata-rata nilai

    st.write(f"**Rata-rata Nilai Robby:** {rata_rata:.2f}")

    # **Visualisasi Data Nilai Robby**
    data = {
        'Mata Kuliah': robby_scores.columns.tolist(),
        'Nilai': robby_scores.iloc[0].tolist()
    }
    robby_scores_df = pd.DataFrame(data)

    # Plot menggunakan Plotly
    fig = px.bar(
        robby_scores_df,
        x='Mata Kuliah',
        y='Nilai',
        title="Nilai Robby per Mata Kuliah",
        labels={'Nilai': 'Skor', 'Mata Kuliah': 'Mata Kuliah'},
        color='Nilai',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# **Select Data berdasarkan Nama Mahasiswa**
st.subheader("Detail Matakuliah dan nilai rata-rata Nilai")

# Pilih data berdasarkan nama
name_options = load["Name"].unique()  # Mengambil semua nama yang ada di dataset
selected_name = st.selectbox("Pilih Nama Mahasiswa:", options=name_options)

# Filter data berdasarkan nama yang dipilih
filtered_data = load[load["Name"] == selected_name]

if not filtered_data.empty:
    st.write(f"**Detail Data untuk {selected_name}:**")
    st.dataframe(filtered_data)

    # Hitung rata-rata nilai (opsional)
    nilai_data = filtered_data.iloc[:, 1:]  # Ambil kolom nilai (mata kuliah dan skor)
    rata_rata = nilai_data.mean(axis=1).iloc[0]

    # Tampilkan rata-rata nilai
    st.write(f"Rata-rata Nilai {selected_name}: **{rata_rata:.2f}**")
    
    # Visualisasi Nilai dengan Bar Chart
    nilai_dict = {
        "Mata Kuliah": nilai_data.columns.tolist(),
        "Nilai": nilai_data.iloc[0].tolist()
    }
    nilai_df = pd.DataFrame(nilai_dict)

    fig = px.bar(
        nilai_df,
        x="Mata Kuliah",
        y="Nilai",
        title=f"Nilai Mata Kuliah {selected_name}",
        labels={"Nilai": "Skor", "Mata Kuliah": "Mata Kuliah"},
        color="Nilai",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"Data untuk {selected_name} tidak ditemukan.")
