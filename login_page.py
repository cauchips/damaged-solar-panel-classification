import streamlit as st
import sqlite3
import bcrypt


def login():
    st.markdown("<h2 style='text-align: center; color: #C5C8C6;'>Login</h2>", unsafe_allow_html=True)

    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    # Cek apakah ada username dan password tersimpan, jika tidak tambahkan admin default
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    admin_exists = c.fetchone()

    if not admin_exists:
        admin_password_hash = bcrypt.hashpw('admin'.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ('admin', admin_password_hash.decode()))
        conn.commit()

    # Cek username dan password
    username = st.text_input("Username", placeholder="Masukkan username Anda")
    password = st.text_input("Password", type="password", placeholder="Masukkan password Anda")

    if st.button("Login"):
        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()

        if user_data and bcrypt.checkpw(password.encode(), user_data[0].encode()):
            st.success("Login berhasil!")
            return True
        else:
            st.error("Login gagal, periksa kembali username dan password!")
            return False

    return False
