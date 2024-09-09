import os
import subprocess

# Fungsi untuk menjalankan subfinder dan httpx
def run_subfinder_httpx(input_file, is_domain_list=False):
    try:
        if is_domain_list:
            subfinder_cmd = f"subfinder -dL {input_file} -silent -o subfinder_output.txt"
        else:
            subfinder_cmd = f"subfinder -d {input_file} -silent -o subfinder_output.txt"

        # Jalankan subfinder
        print(f"Menjalankan: {subfinder_cmd}")
        subprocess.run(subfinder_cmd, shell=True)

        # Jalankan httpx
        httpx_cmd = "httpx-toolkit -l subfinder_output.txt -silent -o httpx_output.txt"
        print(f"Menjalankan: {httpx_cmd}")
        subprocess.run(httpx_cmd, shell=True)

    except Exception as e:
        print(f"Kesalahan saat menjalankan subfinder atau httpx: {e}")

# Fungsi untuk menyaring subdomain yang tidak diinginkan dan menambahkan 'https://'
def filter_subdomains_and_add_https(input_file, output_file):
    unwanted_subdomains = ['autodiscover', 'cpanel', 'cpcalendars', 'webmail', 'demo', 
                           'beta', 'cpcontacts', 'mail', 'webdisk', 'www', 'slot']

    try:
        with open(input_file, 'r') as file:
            filtered_domains = set()  # Menggunakan set untuk menghapus duplikat
            for line in file:
                domain = line.strip()

                # Periksa apakah domain mengandung subdomain yang tidak diinginkan
                if not any(sub in domain for sub in unwanted_subdomains):
                    # Jika domain sudah memiliki https:// atau http://, jangan ditambahkan lagi
                    if not domain.startswith("https://") and not domain.startswith("http://"):
                        domain = f"https://{domain}"
                    filtered_domains.add(domain)

        with open(output_file, 'w') as file:
            for domain in sorted(filtered_domains):
                file.write(domain + '\n')

        print(f"Domain yang difilter dan diurutkan disimpan di {output_file}")
    except Exception as e:
        print(f"Kesalahan saat menyaring subdomain: {e}")

# Fungsi untuk mencari query dengan Katana atau Paramspider
def search_with_katana_or_paramspider(output_file):
    try:
        tool_choice = input("Pilih tool (katana/paramspider): ").lower()

        # Cek apakah file input (output dari httpx) ada
        if not os.path.exists(output_file):
            print(f"File {output_file} tidak ditemukan.")
            return

        with open(output_file, 'r') as file:
            lines = file.readlines()
            # Pastikan file tidak kosong dan berisi URL yang valid
            if len(lines) == 0:
                print(f"File {output_file} kosong. Pastikan file memiliki domain yang valid.")
                return
            else:
                # Cek apakah setiap baris adalah URL yang valid
                for line in lines:
                    if not line.startswith("http://") and not line.startswith("https://"):
                        print(f"URL tidak valid di file: {line.strip()}")
                        return

        # Jalankan Katana atau Paramspider berdasarkan pilihan
        if tool_choice == "katana":
            cmd = f"katana -d 5 -ps -pss waybackarchive, commoncrawl, alienvault -f qurl -u {output_file} -o katana_output.txt"
        elif tool_choice == "paramspider":
            cmd = f"paramspider -dL {output_file} -o paramspider_output.txt"
        else:
            print("Tool tidak valid!")
            return

        # Menjalankan tool yang dipilih
        print(f"Menjalankan: {cmd}")
        subprocess.run(cmd, shell=True)

        # Setelah menjalankan, periksa apakah output file dari Katana/Paramspider berhasil dibuat
        output_result_file = 'katana_output.txt' if tool_choice == "katana" else 'paramspider_output.txt'

        if not os.path.exists(output_result_file):
            print(f"Kesalahan: Output file {output_result_file} tidak ditemukan.")
            return

        # Filter domain dengan '?id=' dan simpan hasilnya
        with open(output_result_file, 'r') as file:
            query_domains = [line.strip() for line in file if '?id=' in line]

        if query_domains:
            with open('query_filtered_domains.txt', 'w') as output:
                for domain in query_domains:
                    output.write(domain + '\n')
            print("Domain dengan '?id=' disimpan di query_filtered_domains.txt")
        else:
            print("Tidak ada domain yang mengandung '?id=' ditemukan.")

    except Exception as e:
        print(f"Kesalahan saat mencari query: {e}")

# Fungsi untuk menjalankan Nuclei
def run_nuclei(input_file):
    try:
        nuclei_cmd = f"nuclei -t templates -severity low,medium,high,critical -l {input_file} -o nuclei_output.txt"
        print(f"Menjalankan: {nuclei_cmd}")
        subprocess.run(nuclei_cmd, shell=True)
    except Exception as e:
        print(f"Kesalahan saat menjalankan Nuclei: {e}")

# Main function
def main():
    domain_input = input("Masukkan nama domain atau file list: ")
    is_domain_list = domain_input.endswith('.txt')

    # Jalankan subfinder dan httpx
    run_subfinder_httpx(domain_input, is_domain_list)

    # Filter subdomain yang tidak diinginkan dan tambahkan 'https://'
    filter_subdomains_and_add_https('httpx_output.txt', 'filtered_domains.txt')

    # Pilih opsi setelah filtering
    print("\nPilih Opsi:")
    print("1. Cari query dengan Katana atau Paramspider")
    print("2. Langsung jalankan Nuclei")
    option = input("Pilih opsi (1/2): ")

    if option == '1':
        search_with_katana_or_paramspider('filtered_domains.txt')
    elif option == '2':
        run_nuclei('filtered_domains.txt')
    else:
        print("Opsi tidak valid.")

if __name__ == "__main__":
    main()
