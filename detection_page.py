import streamlit as st
from PIL import Image, ImageDraw
import tensorflow as tf
import numpy as np
import io
from datetime import datetime
import sqlite3


@st.cache_resource
def load_model():
    return tf.keras.models.load_model('model.keras', safe_mode=False)


def detect_panel_damage():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    model = load_model()

    st.markdown("<h3 style='text-align: center; color: #C5C8C6;'>Deteksi Kerusakan Panel Surya</h3>",
                unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Unggah gambar panel surya", type=["jpg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
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
                cropped_images.append((cropped_image, (left, upper, right, lower)))

        damage_scores = 0
        total_confidence = 0
        draw = ImageDraw.Draw(image)

        for cropped_image, box in cropped_images:
            cropped_image = cropped_image.resize((299, 299))
            image_array = tf.keras.preprocessing.image.img_to_array(cropped_image)
            image_array = np.expand_dims(image_array, axis=0)
            image_array /= 255.0

            prediction = model.predict(image_array)
            confidence = prediction[0][0]

            if confidence < 0.5:
                adjusted_confidence = 100 - (confidence * 100)
                damage_scores += 1
                draw.rectangle(box, outline="green", width=3)
            else:
                adjusted_confidence = confidence * 100

            total_confidence += adjusted_confidence

        avg_confidence = total_confidence / 20
        label = "Kerusakan Berat" if damage_scores > 10 else (
            "Kerusakan Ringan" if damage_scores > 0 else "Tidak Rusak")

        image_name = uploaded_file.name
        st.image(image, caption=image_name, use_column_width=True)
        st.write(f"Klasifikasi: {label}")
        st.write(f"Jumlah panel rusak: {damage_scores}/20")
        st.write(f"Tingkat akurasi: {avg_confidence:.2f}%")

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_data = img_byte_arr.getvalue()

        current_date = datetime.now().strftime("%d %b %Y, %I:%M %p")
        c.execute(
            "INSERT INTO history (image_name, label, image, damage_count, avg_confidence, date) VALUES (?, ?, ?, ?, ?, ?)",
            (image_name, label, img_byte_data, int(damage_scores), avg_confidence, current_date))
        conn.commit()
    conn.close()
