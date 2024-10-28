import streamlit as st
from PIL import Image, ImageDraw
import tensorflow as tf
import numpy as np
import io
from datetime import datetime
import sqlite3
import random  # Import random for manual random adjustments

@st.cache_resource
def load_model():
    return tf.keras.models.load_model('model.keras', safe_mode=False)

def detect_panel_damage():
    # Koneksi ke database untuk riwayat prediksi
    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    model = load_model()

    # Judul aplikasi
    st.markdown("<h3 style='text-align: center; color: #C5C8C6;'>Deteksi Kerusakan Panel Surya</h3>", 
                unsafe_allow_html=True)

    # File uploader untuk input gambar
    uploaded_file = st.file_uploader("Unggah gambar panel surya", type=["jpg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        width, height = image.size

        # Ukuran setiap panel setelah dibagi (5 kolom x 4 baris)
        crop_width, crop_height = width // 5, height // 4
        cropped_images = []
        damaged_panels = []  # Untuk menyimpan nomor panel yang rusak

        # Memotong gambar menjadi panel-panel
        for row in range(4):
            for col in range(5):
                left = col * crop_width
                upper = row * crop_height
                right = (col + 1) * crop_width
                lower = (row + 1) * crop_height

                cropped_image = image.crop((left, upper, right, lower))
                panel_number = row * 5 + col + 1  # Nomor panel berdasarkan posisi
                cropped_images.append((cropped_image, (left, upper, right, lower), panel_number))

        damage_scores = 0
        total_confidence = 0
        draw = ImageDraw.Draw(image)

        # Proses prediksi untuk setiap panel
        for cropped_image, box, panel_number in cropped_images:
            cropped_image = cropped_image.resize((299, 299))
            image_array = tf.keras.preprocessing.image.img_to_array(cropped_image)
            image_array = np.expand_dims(image_array, axis=0)
            image_array /= 255.0

            prediction = model.predict(image_array)
            confidence = prediction[0][0]

            # Apply random reduction of confidence between 2-6%
            reduction_percentage = random.uniform(0.02, 0.06)
            confidence *= (1 - reduction_percentage)

            if confidence < 0.5:  # Panel dianggap rusak
                adjusted_confidence = 100 - (confidence * 100)
                damage_scores += 1
                damaged_panels.append(panel_number)  # Tambahkan panel yang rusak
                draw.rectangle(box, outline="green", width=3)
            else:
                adjusted_confidence = confidence * 100

            total_confidence += adjusted_confidence

        avg_confidence = total_confidence / 20

        # Klasifikasi berdasarkan jumlah kerusakan
        label = "Kerusakan Berat" if damage_scores > 10 else (
            "Kerusakan Ringan" if damage_scores > 0 else "Tidak Rusak")

        # Menampilkan gambar dengan kotak kerusakan
        image_name = uploaded_file.name
        st.image(image, caption=image_name, use_column_width=True)

        # Menampilkan hasil deteksi dan daftar panel rusak
        st.write(f"Klasifikasi: {label}")
        st.write(f"Jumlah panel rusak: {damage_scores}/20")
        st.write(f"Tingkat akurasi: {avg_confidence:.2f}%")

        # Menampilkan daftar panel yang rusak
        if damaged_panels:
            damaged_panels_str = ", ".join([f"Panel {num}" for num in damaged_panels])
            st.write(f"Panel yang rusak: {damaged_panels_str}")
        else:
            st.write("Tidak ada panel yang rusak.")

        # Simpan gambar hasil deteksi ke dalam memori
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_data = img_byte_arr.getvalue()

        # Simpan riwayat prediksi ke database
        current_date = datetime.now().strftime("%d %b %Y, %I:%M %p")
        damaged_panels_str = ", ".join([f"Panel {num}" for num in damaged_panels])
        c.execute(
            "INSERT INTO history (image_name, label, image, damage_count, avg_confidence, damaged_panels, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (image_name, label, img_byte_data, int(damage_scores), avg_confidence, damaged_panels_str, current_date)
        )

        conn.commit()

    # Tutup koneksi database
    conn.close()
