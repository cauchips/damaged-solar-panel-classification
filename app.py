import streamlit as st

st.set_page_config(page_title="Aplikasi Deteksi Kerusakan Panel Surya", initial_sidebar_state="expanded", page_icon="🌞")

from login_page import login
from tutorial_page import show_tutorial
from detection_page import detect_panel_damage
from history_page import show_history

# Logo di bagian paling atas halaman
col1, col2 = st.columns([1, 8])
with col1:
    st.image("media/logo-2.png", width=70)
with col2:
    st.image("media/logo-1.png", width=330)
st.markdown("<h2 style='text-align: center; color: #81A2BE ;'>Aplikasi Deteksi Kerusakan Panel Surya</h2>", unsafe_allow_html=True)


# Periksa apakah pengguna sudah login dengan session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Jika belum login, tampilkan halaman login
if not st.session_state['logged_in']:
    if login():
        st.session_state['logged_in'] = True  # Set session state menjadi True setelah login berhasil
        st.success("Klik tombol Login lagi untuk melanjutkan!")
else:
    # Sidebar navigasi
    st.sidebar.title("Navigasi")
    page = st.sidebar.selectbox("Pilih halaman", ["Tutorial", "Deteksi Kerusakan", "Riwayat Prediksi"])

    # Navigasi antar halaman
    if page == "Tutorial":
        show_tutorial()
    elif page == "Deteksi Kerusakan":
        detect_panel_damage()
    elif page == "Riwayat Prediksi":
        show_history()

# Tombol logout
if st.session_state['logged_in']:
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False  # Reset session state jika logout
        st.rerun()  # Muat ulang halaman setelah logout
