import streamlit as st

def show_tutorial():
    # Judul tutorial dengan tampilan lebih besar
    st.markdown("<h3 style='text-align: center; color: #C5C8C6;'>Tutorial Cara Penggunaan Aplikasi</h3>", unsafe_allow_html=True)

    # Tambahkan informasi navigasi dengan ikon untuk memperindah
    st.markdown("""
    <div style='background-color: #1A1A2E; padding: 15px; border-radius: 10px;'>
        <h4 style='color: #D6DBDF;'>🚀 Navigasi Aplikasi</h4>
        <ul>
            Gunakan <b>Sidebar</b> di sebelah kiri untuk beralih antara halaman:
            <ul style='line-height: 1.6;'>
                <li><b>Tutorial</b>: Menampilkan petunjuk cara menggunakan aplikasi.</li>
                <li><b>Deteksi Kerusakan</b>: Untuk mengunggah gambar panel surya dan melakukan deteksi.</li>
                <li><b>Riwayat Prediksi</b>: Melihat hasil prediksi sebelumnya.</li>
            </ul>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Deskripsi langkah-langkah penggunaan
    st.markdown("""
    <div style='padding: 15px;'>
        <h4 style='color: #D6DBDF;'>📋 Langkah-langkah Penggunaan</h4>
        <ol style='line-height: 1.8;'>
            <li>Gunakan gambar panel surya tipe <b>Thin Film</b>.</li>
            <li>Gambar panel dibatasi dengan jumlah 20 panel yang terdiri dari 5 panel pada lebar dan 4 panel pada tinggi.</li>
            <li>Berikut adalah contoh gambar:</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # Tampilkan gambar petunjuk pemetaan yang diunggah
    st.image("media/petunjuk.jpg", caption="📋 Petunjuk Pemetaan", use_column_width=True)

    # Keterangan panel dengan lokasi pemetaan dan penomoran
    st.markdown("""
    <div style='padding: 15px;'>
        <h4 style='color: #D6DBDF;'>📍 Keterangan Pemetaan Panel</h4>
        <p>Panel-panel dipetakan dalam matriks 5x4 (5 kolom dan 4 baris) dengan nomor urut seperti contoh di atas. Berikut adalah penjelasan lokasi penomoran:</p>
        <table style='border: 1px solid #D6DBDF; border-collapse: collapse; width: 100%; text-align: center;'>
            <tr>
                <th style='border: 1px solid #D6DBDF; padding: 10px;'>Baris/ Kolom</th>
                <th style='border: 1px solid #D6DBDF; padding: 10px;'>Nomor Panel</th>
            </tr>
            <tr>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>Baris 1</td>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>1, 2, 3, 4, 5</td>
            </tr>
            <tr>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>Baris 2</td>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>6, 7, 8, 9, 10</td>
            </tr>
            <tr>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>Baris 3</td>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>11, 12, 13, 14, 15</td>
            </tr>
            <tr>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>Baris 4</td>
                <td style='border: 1px solid #D6DBDF; padding: 10px;'>16, 17, 18, 19, 20</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Kolom untuk menampilkan contoh gambar RGB dan Grayscale
    col1, col2, col3, col4 = st.columns(4)

    with col2:
        st.image("media/contoh-rgb.jpg", caption="🌈 Gambar RGB", use_column_width=True)

    with col3:
        st.image("media/contoh-grayscale.jpg", caption="⚫ Gambar Grayscale", use_column_width=True)

    # Langkah-langkah tambahan setelah gambar
    st.markdown("""
    <div style='padding: 15px;'>
        <ol start="4" style='line-height: 1.8;'>
            <li>Setelah sudah sesuai pada langkah ke 1 hingga 3, silahkan mengunggah di sidebar <b>Deteksi Kerusakan</b> kemudian input gambar pada area <b>"Drag and drop file here"</b> atau tombol <b>"Browse files"</b>.</li>
            <li>Tunggu beberapa saat hingga hasil deteksi kerusakan dan jumlah kerusakan panel ditampilkan pada layar.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

