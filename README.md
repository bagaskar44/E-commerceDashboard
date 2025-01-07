# E-commerceDashboard
Proyek dashboard analisis data, studi kasus dataset e-commerce untuk proyek analisis data ID Camp.

## Fitur
- Analisis data dari dataset.
- Visualisasi data hasil analisis menggunakan chart.
- Dashboard interaktif.

## Struktur Proyek
```
|-- dashboard.py          # File utama untuk menjalankan dashboard
|-- dataset.csv           # File dataset yang digunakan
|-- requirements.txt      # Dependensi yang diperlukan
```

## Cara Instalasi
1. **Clone repositori**:
   ```
   git clone https://github.com/bagaskar44/E-commerceDashboard.git
   cd E-commerceDashboard
   ```

2. **Instal dependensi**:
   ```
   pip install -r requirements.txt
   ```

## Cara Menjalankan
1. Pastikan semua dependensi terinstal.
2. Jalankan file `dashboard.py`:
   ```
   streamlit run dashboard.py
   ```
   
## Link Demo Online
Dashboard ini juga tersedia secara online melalui Streamlit Cloud. Anda dapat mengaksesnya di tautan berikut:
https://e-commercedashboardidcamp.streamlit.app/ 

## Dataset
File `dataset.csv` adalah dataset yang digunakan untuk analisis. Ini berisi beberapa dataset berikut:
- **cust_each_location_part1**: Kombinasi latitude dan longitude yang menunjukan lokasi setiap pelanggan bagian 1.
- **cust_each_location_part2**: Kombinasi latitude dan longitude yang menunjukan lokasi setiap pelanggan bagian 2.
- **odr_itm_paymnt_timestmp_df_part1**: Semua informasi terkait order yang dilakukan oleh pelanggan bagian 1.
- **odr_itm_paymnt_timestmp_df_part2**: Semua informasi terkait order yang dilakukan oleh pelanggan bagian 2.
- **order_with_payments_df**: Informasi order dan pembayaran.
- **product_category_name_df**: Nama kategori produk
- **products_df**: Semua informasi tentang produk


