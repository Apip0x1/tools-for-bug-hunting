kalian bisa recode tools ini untuk perintah yang kalian ingin jalankan.

Fitur-fitur
### 1. **Subdomain Enumeration (Subfinder + Httpx Integration)**
   - **Deskripsi**: Script ini akan menjalankan `subfinder` untuk mendapatkan subdomain dari sebuah domain atau daftar domain yang Anda masukkan, kemudian langsung menjalankan `httpx` untuk memverifikasi status dari setiap subdomain yang ditemukan.
   - **Fungsi yang digunakan**: 
     - `run_subfinder_httpx(input_file, is_domain_list=False)`

### 2. **Filter Subdomain yang Tidak Diinginkan**
   - **Deskripsi**: Setelah mendapatkan hasil dari `httpx`, script ini akan memfilter subdomain yang tidak diinginkan seperti `autodiscover`, `cpanel`, `cpcalendars`, `webmail`, dll. Selain itu, script ini juga akan menambahkan `https://` di setiap domain yang belum memiliki protokol `https://` atau `http://`.
   - **Subdomain yang dihilangkan**: `autodiscover, cpanel, cpcalendars, webmail, demo, beta, cpcontacts, mail, webdisk, www`, serta subdomain yang mengandung kata `slot`.
   - **Fungsi yang digunakan**:
     - `filter_subdomains_and_add_https(input_file, output_file)`

### 3. **Pencarian Query dengan Katana atau Paramspider**
   - **Deskripsi**: Anda bisa memilih untuk mencari query yang mengandung parameter `?id=` menggunakan salah satu dari dua tools:
     - **Katana**: Menggunakan berbagai sumber (seperti Wayback Machine, Common Crawl, AlienVault) untuk mencari URL yang mengandung parameter.
     - **Paramspider**: Tool pencari parameter di subdomain yang telah difilter.
   - **Output**: Hanya domain yang mengandung parameter `?id=` akan disimpan dalam file `query_filtered_domains.txt`.
   - **Fungsi yang digunakan**:
     - `search_with_katana_or_paramspider(output_file)`

### 4. **Scanning dengan Nuclei**
   - **Deskripsi**: Alternatif pilihan dari fitur pencarian query, script ini bisa langsung menjalankan scanning kerentanan menggunakan `Nuclei`. Nuclei akan menjalankan template-template yang sesuai dengan severity level (rendah, sedang, tinggi, kritis).
   - **Output**: Hasil scan disimpan dalam `nuclei_output.txt`.
   - **Fungsi yang digunakan**:
     - `run_nuclei(input_file)`

### 5. **Dua Opsi untuk Proses Selanjutnya**
   Setelah melakukan filtering, pengguna diberikan dua opsi untuk proses lebih lanjut:
   - **Opsi 1**: Mencari query dengan `Katana` atau `Paramspider`, menyimpan domain yang memiliki parameter `?id=`.
   - **Opsi 2**: Langsung melakukan scan kerentanan dengan `Nuclei`.
   - **Fungsi yang digunakan**:
     - `main()`

### 6. **Penggunaan Set untuk Menghindari Duplikasi**
   - **Deskripsi**: Setiap domain yang telah difilter akan disimpan dalam bentuk `set`, sehingga duplikasi domain secara otomatis dihilangkan.

### 7. **Validasi Domain pada Output File**
   - **Deskripsi**: Script memastikan bahwa domain yang ditemukan dari output `httpx` adalah URL yang valid sebelum diteruskan ke tools lain. Jika ada URL yang tidak valid, program akan memberikan peringatan.

### **Alur Kerja Tools**:
1. Pengguna memasukkan domain atau daftar domain.
2. Tools menjalankan `subfinder` untuk menemukan subdomain, dan `httpx` untuk mengecek status domain.
3. Subdomain yang tidak diinginkan akan dihilangkan, dan protokol `https://` akan ditambahkan jika diperlukan.
4. Pengguna memilih salah satu dari dua opsi:
   - **Opsi 1**: Mencari query menggunakan `Katana` atau `Paramspider`.
   - **Opsi 2**: Menjalankan scan kerentanan dengan `Nuclei`.

Dengan fitur-fitur di atas, tools ini memungkinkan untuk melakukan enumerasi subdomain, memfilter yang tidak diinginkan, mencari parameter query, dan melakukan scanning kerentanan secara otomatis.
