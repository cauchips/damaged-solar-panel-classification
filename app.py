import numpy as np
import sqlite3
import tensorflow as tf
import streamlit as st
from PIL import Image
import io  # For handling byte data
from datetime import datetime  # To handle date and time

# SQLite database setup
conn = sqlite3.connect('hist.db')
c = conn.cursor()

# Add a 'date' column of type TEXT to store the date of prediction
c.execute('''CREATE TABLE IF NOT EXISTS history
             (image_name TEXT, label TEXT, image BLOB, damage_count INTEGER, date TEXT)''')

# Load the model (replace 'model.keras' with your actual model path)
model = tf.keras.models.load_model('best_model.keras')

# Streamlit UI
st.title("Solar Panel Damage Classification")

# Image upload
uploaded_file = st.file_uploader("Upload a solar panel image", type=["jpg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Convert image to binary data (BLOB)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # Use PNG format to avoid issues with image formats
    img_byte_data = img_byte_arr.getvalue()  # This will be saved to the database as BLOB

    # Crop the image into 5 columns and 4 rows (20 sections)
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
            cropped_images.append(cropped_image)

    # Preprocess and predict for each cropped image
    damage_scores = 0

    for cropped_image in cropped_images:
        cropped_image = cropped_image.resize((160, 160))
        image_array = tf.keras.preprocessing.image.img_to_array(cropped_image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array /= 255.0

        # Predict damage
        prediction = model.predict(image_array)
        confidence = prediction[0][0]
        if confidence < 0.5:
            damage_scores += 1  # Increment damage scores when section is damaged

    # Classify based on the number of damaged sections
    if damage_scores == 0:
        label = "No Damage"
    elif 1 <= damage_scores <= 10:
        label = "Minor Damage"
    else:
        label = "Severe Damage"

    image_name = uploaded_file.name
    # Display the result
    st.image(image, caption=image_name, use_column_width=True)
    st.write(f"Classification: {label}")
    st.write(f"Damaged panels: {damage_scores}/20")

    # Get the current date and time in a readable format (e.g., 20 Sep 2024, 03:30 PM)
    current_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # Save to database (image name, label, image blob, damage count, and date)
    c.execute("INSERT INTO history (image_name, label, image, damage_count, date) VALUES (?, ?, ?, ?, ?)",
              (image_name, label, img_byte_data, int(damage_scores), current_date))  # Include the formatted date
    conn.commit()

# Display history
st.subheader("Prediction History")

# Modify SQL query to retrieve history ordered by date in descending order (most recent first)
history = c.execute("SELECT * FROM history ORDER BY date DESC").fetchall()

if history:
    for row in history:
        image_name = row[0]
        label = row[1]
        image_data = row[2]  # Retrieve the BLOB data (binary image data)
        damage_count = int(row[3])  # Ensure the damage count is an integer
        date = row[4]  # Retrieve the date

        # Convert the BLOB data back into an image
        img = Image.open(io.BytesIO(image_data))  # Convert binary data to image

        # Display the history using a clean, structured layout
        col1, col2 = st.columns([1, 2])  # 1/3 image, 2/3 text
        with col1:
            st.image(img, caption=image_name, use_column_width=True)

        with col2:
            st.write(f"**Classification**: {label}")
            st.write(f"**Damaged Panels**: {damage_count}/20")
            st.write(f"**Date**: {date}")

        # Add a horizontal line to separate entries
        st.markdown("---")
else:
    st.write("No predictions yet.")

# Close the database connection on exit
conn.close()