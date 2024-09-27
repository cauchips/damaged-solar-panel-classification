import numpy as np
import sqlite3
import tensorflow as tf
import streamlit as st
from PIL import Image, ImageDraw
import io
from datetime import datetime

# Koneksi ke database SQLite
conn = sqlite3.connect('history.db')
c = conn.cursor()

# Buat tabel untuk menyimpan riwayat prediksi jika belum ada
c.execute('''CREATE TABLE IF NOT EXISTS history
             (image_name TEXT, label TEXT, image BLOB, damage_count INTEGER, avg_confidence REAL, date TEXT)''')

# Muat model
model = tf.keras.models.load_model('model.keras', safe_mode=False)

# Streamlit UI untuk unggah gambar
st.title("Deteksi Kerusakan Panel Surya")
uploaded_file = st.file_uploader("Unggah gambar panel surya", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Potong gambar jadi 5 kolom dan 4 baris
    width, height = image.size
    cropped_images = []
    crop_width, crop_height = width // 5, height // 4

    for row in range(4):
        for col in range(5):
            left = col * crop_width
            upper = row * crop_height
            right = (col + 1) * crop_width
            lower = (row + 1) * crop_height
            cropped_image = image.crop((left, upper, right, lower))
            cropped_images.append((cropped_image, (left, upper, right, lower)))  # Simpan posisi

    damage_scores = 0
    total_confidence = 0
    draw = ImageDraw.Draw(image)  # Untuk gambar bounding box

    # Prediksi tiap bagian
    for cropped_image, box in cropped_images:
        cropped_image = cropped_image.resize((299, 299))
        image_array = tf.keras.preprocessing.image.img_to_array(cropped_image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array /= 255.0

        # Prediksi model
        prediction = model.predict(image_array)
        confidence = prediction[0][0]

        # Jika confidence < 0.5 (indicates damage), gunakan 100 - confidence
        if confidence < 0.5:
            adjusted_confidence = 100 - (confidence * 100)
            damage_scores += 1  # Tambahkan ke hitungan kerusakan
            draw.rectangle(box, outline="green", width=2)  # Gambar bounding box hijau
        else:
            adjusted_confidence = confidence * 100

        # Tambahkan confidence (adjusted atau asli) ke total
        total_confidence += adjusted_confidence

    # Hitung rerata confidence rate (menggunakan total yang disesuaikan)
    avg_confidence = total_confidence / 20

    # Tentukan label kerusakan
    if damage_scores == 0:
        label = "Tidak Rusak"
    elif 1 <= damage_scores <= 10:
        label = "Kerusakan Ringan"
    else:
        label = "Kerusakan Berat"

    image_name = uploaded_file.name

    # Tampilkan hasil
    st.image(image, caption=image_name, use_column_width=True)
    st.write(f"Klasifikasi: {label}")
    st.write(f"Jumlah panel rusak: {damage_scores}/20")
    st.write(f"Rata-rata tingkat keyakinan: {avg_confidence:.2f}%")

    # Konversi gambar hasil (yang sudah ada bounding box) ke format BLOB
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_data = img_byte_arr.getvalue()

    # Dapatkan tanggal saat ini
    current_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # Simpan gambar yang sudah diberi bounding box dan informasi ke database
    c.execute("INSERT INTO history (image_name, label, image, damage_count, avg_confidence, date) VALUES (?, ?, ?, ?, ?, ?)",
              (image_name, label, img_byte_data, int(damage_scores), avg_confidence, current_date))
    conn.commit()

# Tampilkan riwayat prediksi
st.subheader("Riwayat Prediksi")
history = c.execute("SELECT * FROM history ORDER BY date DESC").fetchall()

if history:
    for row in history:
        image_name = row[0]
        label = row[1]
        image_data = row[2]
        damage_count = int(row[3])
        avg_confidence = float(row[4])
        date = row[5]

        # Konversi BLOB ke gambar
        img = Image.open(io.BytesIO(image_data))

        # Tampilkan riwayat
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(img, caption=image_name, use_column_width=True)

        with col2:
            st.write(f"**Klasifikasi**: {label}")
            st.write(f"**Panel Rusak**: {damage_count}/20")
            st.write(f"**Rata-rata tingkat keyakinan**: {avg_confidence:.2f}%")
            st.write(f"**Tanggal**: {date}")

        st.markdown("---")
else:
    st.write("Belum ada prediksi.")

# Tutup koneksi database
conn.close()
