import streamlit as st
import sqlite3
from PIL import Image
import io

def show_history():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    st.markdown("<h3 style='text-align: center; color: #C5C8C6;'>Riwayat Prediksi</h3>", unsafe_allow_html=True)
    st.text("")
    history = c.execute("SELECT * FROM history ORDER BY date DESC").fetchall()

    if history:
        for row in history:
            image_name = row[0]
            label = row[1]
            image_data = row[2]
            damage_count = int(row[3])
            avg_confidence = float(row[4])
            date = row[5]

            img = Image.open(io.BytesIO(image_data))

            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img, caption=image_name, use_column_width=True)
            with col2:
                st.write(f"**Klasifikasi**: {label}")
                st.write(f"**Jumlah Panel Rusak**: {damage_count}/20")
                st.write(f"**Tingkat Akurasi**: {avg_confidence:.2f}%")
                st.write(f"**Tanggal**: {date}")
            st.markdown("---")
    else:
        st.write("Belum ada prediksi.")
    conn.close()