import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Input Data Dosen dan Daris")

st.title("📋 Input Data Dosen dan Daris")

# Form Input
with st.form("form_input"):
    nama_daris = st.text_input("👤 Nama Daris")
    nama_dosen = st.text_input("👨‍🏫 Nama Dosen")
    tanggal = st.date_input("📅 Tanggal", format="DD-MM-YYYY")
    waktu = st.time_input("⏰ Waktu")
    lokasi = st.radio("📍 Lokasi", ["KAMPUS 1", "KAMPUS 2", "KAMPUS 3", "Online"])

    submitted = st.form_submit_button("Simpan Data")

# Simpan ke CSV
if submitted:
    if not all([nama_daris, nama_dosen]):
        st.warning("Mohon isi semua field!")
    else:
        data_baru = {
            "Nama Daris": nama_daris,
            "Nama Dosen": nama_dosen,
            "Tanggal": tanggal.strftime("%Y-%m-%d"),
            "Waktu": waktu.strftime("%H:%M"),
            "Lokasi": lokasi
        }

        try:
            df_lama = pd.read_csv("data_dosen.csv")
        except FileNotFoundError:
            df_lama = pd.DataFrame()

        df_baru = pd.concat([df_lama, pd.DataFrame([data_baru])], ignore_index=True)
        df_baru.to_csv("data_dosen.csv", index=False)

        st.success("✅ Data berhasil disimpan!")

        with st.expander("📄 Lihat Data Terkini"):
            st.dataframe(df_baru)
    # Tampilkan data
st.markdown("## 📄 Data yang Sudah Tersimpan")

try:
    df_tersimpan = pd.read_csv("data_dosen.csv")

    st.markdown("### 🔎 Filter Data")

    # Input filter
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_daris = st.text_input("Cari Nama Daris")
    with col2:
        filter_dosen = st.text_input("Cari Nama Dosen")
    with col3:
        filter_tanggal = st.date_input("Filter Tanggal", value=None)

    # Terapkan filter
    df_filtered = df_tersimpan.copy()

    if filter_daris:
        df_filtered = df_filtered[df_filtered['Nama Daris'].str.contains(filter_daris, case=False, na=False)]

    if filter_dosen:
        df_filtered = df_filtered[df_filtered['Nama Dosen'].str.contains(filter_dosen, case=False, na=False)]

    if filter_tanggal:
        df_filtered = df_filtered[df_filtered['Tanggal'] == filter_tanggal.strftime("%Y-%m-%d")]

    st.markdown("### 📋 Hasil Filter")
    st.dataframe(df_filtered)

except FileNotFoundError:
    st.info("Belum ada data yang tersimpan.")

