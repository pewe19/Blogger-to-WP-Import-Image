# Blogger to WP Import Image [Only Image]
Script Python: Import file image dari data di blogspot/blogger lalu di export ke wordpress. Otomatis mengubah file .jpg dan .png di conver ke .webp

## Script ini melakukan:

### [1.] Ekstraksi URL gambar dari Blogspot:
- Mengambil semua URL gambar dari blog
- Memfilter hanya file .jpg dan .png

### [2.] Proses konversi:
- Mengunduh setiap gambar
- Mengkonversi ke format WebP
- Mengkompresi dengan quality 65% (bisa disesuaikan)

### [3.] Upload ke WordPress:
- Menggunakan WordPress XML-RPC API
- Menyimpan gambar ke Media Library

### [4.] Logging dan Error Handling:
- Membuat log CSV dengan status setiap proses
- Mencatat URL asli dan URL WordPress
- Menangani error untuk setiap gambar

### Untuk menjalankan script
- Install dependencies:

<code> pip install requests beautifulsoup4 Pillow python-wordpress-xmlrpc </code>

## Sesuaikan konfigurasi di bagian bawah script:
- BLOGSPOT_URL = "https://your-blog.blogspot.com"
- WP_URL = "https://your-wordpress-site.com"
- WP_USERNAME = "your_username"
- WP_PASSWORD = "your_password"

## Aktifkan XML-RPC di WordPress:
- Buka Settings > Writing
- Enable XML-RPC
