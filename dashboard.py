import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import time
from folium.plugins import HeatMap
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard E-Commerce Public",
    page_icon="📊",
    layout="wide",
)

@st.cache_data
def load_cust_each_loc():
    part1 = pd.read_csv('cust_each_location_part1.csv')
    part2 = pd.read_csv('cust_each_location_part2.csv')
    cust_each_location = pd.concat([part1, part2], ignore_index=True)
    # Hanya menggunakan sampel 1000 data random untuk optimalisasi streamlit
    cust_each_location = cust_each_location.sample(n=1000, random_state=7)
    
    return cust_each_location

@st.cache_data
def load_order_with_pay():
    order_with_payments_df = pd.read_csv('order_with_payments_df.csv')
    
    datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
    for column in datetime_columns:
        order_with_payments_df[column] = pd.to_datetime(order_with_payments_df[column])
        
    return order_with_payments_df

@st.cache_data
def load_odr_timestamp():
    part1 = pd.read_csv('odr_itm_paymnt_timestmp_df_part1.csv')
    part2 = pd.read_csv('odr_itm_paymnt_timestmp_df_part2.csv')    
    odr_itm_paymnt_timestmp_df = pd.concat([part1, part2], ignore_index=True)
    
    datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
    for column in datetime_columns:
        odr_itm_paymnt_timestmp_df[column] = pd.to_datetime(odr_itm_paymnt_timestmp_df[column])

    return odr_itm_paymnt_timestmp_df

cust_each_location = load_cust_each_loc()
order_with_payments_df = load_order_with_pay()
odr_itm_paymnt_timestmp_df = load_odr_timestamp()

# Data Untuk Heatmap
@st.cache_data
def load_heat_data():
    # Mengambil data dari dataframe cust_each_location dan cust_geo_df
    heat_data = list(zip(
        cust_each_location['geolocation_lat'],
        cust_each_location['geolocation_lng'],
        cust_each_location['customer_count']
    ))
    return heat_data

heat_data = load_heat_data()

@st.cache_data
def generate_map():
    # Membuat peta folium dengan heatmap
    m = folium.Map(location=['2.946166', '-49.000568'], zoom_start=2)
    HeatMap(heat_data).add_to(m)
    
    return m

m = generate_map()
    
# Data untuk produk dengan revenue terbaik bagi perusahaan
@st.cache_data
def load_productname_revenue(x):
    products_df = pd.read_csv('products_df.csv')
    productname_revenue_df = x.merge(products_df,
                                    on='product_id',
                                    how='inner')
    return productname_revenue_df

@st.cache_data
def load_productname_eng_revenue(x):
    product_category_name_df = pd.read_csv('product_category_name_df.csv')
    productname_eng_revenue_df = x.merge(product_category_name_df,
                                        on='product_category_name',
                                        how='inner')
    return productname_eng_revenue_df

# Data untuk Analisis RFM
@st.cache_data
def load_cust_order_count(x):
    customer_order_count = x.groupby('customer_id')['order_id'].count().reset_index()
    customer_order_count.rename(columns={'order_id': 'order_count'}, inplace=True)
    
    return customer_order_count

@st.cache_data
def load_cust_total_payment(x):
    customer_total_payments = x.groupby('customer_id')['payment_value'].sum().reset_index()
    customer_total_payments.rename(columns={'payment_value': 'total_payment'}, inplace=True)
    
    return customer_total_payments
    
# Sidebar 
st.sidebar.title("📊 Dashboard E-Commerce")
st.sidebar.write("Selamat datang di dashboard! Pilih analisis yang ingin kamu lihat.")

st.sidebar.divider()

# Pilih Analisis
st.sidebar.header("⚙️ Pilih Analisis")
analysis_type = st.sidebar.radio(
    "Pilih tipe analisis:",
    ("Demografi Pelanggan", "Produk Terbaik", "Analisis RFM")
)

# Filter Data Berdasarkan Tanggal
if analysis_type == "Produk Terbaik":
    st.sidebar.divider()
    st.sidebar.header("📅 Filter Data Tanggal")
    start_date = st.sidebar.date_input("🗓️ Tanggal Mulai", value=pd.to_datetime("2017-01-01"))
    end_date = st.sidebar.date_input("📆 Tanggal Akhir", value=pd.to_datetime("2018-12-31"))
    st.sidebar.caption("Pastikan tanggal mulai lebih kecil dari tanggal akhir.")
    
elif analysis_type == "Analisis RFM":
    st.sidebar.divider()
    st.sidebar.header("📅 Filter Data Tanggal")
    start_date = st.sidebar.date_input("🗓️ Tanggal Mulai", value=pd.to_datetime("2017-01-01"))
    end_date = st.sidebar.date_input("📆 Tanggal Akhir", value=pd.to_datetime("2018-12-31"))
    st.sidebar.caption("Pastikan tanggal mulai lebih kecil dari tanggal akhir.")

st.sidebar.divider()
st.sidebar.success("🎉 Happy Analyzing!!!")

# Analisis Demografi Customer dengan Heatmap
if analysis_type == "Demografi Pelanggan":
    # Header untuk heatmap
    st.markdown("## 🌍 Demografi Pelanggan Berdasarkan Wilayah")
    st.markdown("#### 📈 Heatmap Demografi Pelanggan")

    # Menampilkan heatmap pada dashboard
    st_folium(m, width=700, height=500)
    
    # Menampilkan keterangan
    st.caption('*Data berdasarkan 1000 pelanggan random e-commerce untuk pengoptimalan streamlit')
    st.markdown('#### Analisis Demografi Pelanggan E-commerce')
    st.text('Berdasarkan hasil heatmap di atas, terlihat bahwa sebagian besar pelanggan e-commerce terkonsentrasi di wilayah tengah hingga tenggara Brasil. Daerah dengan intensitas warna merah menunjukkan jumlah pelanggan yang paling tinggi, menandakan bahwa aktivitas pelanggan paling signifikan terjadi di pusat-pusat kota atau wilayah padat penduduk di kawasan ini. Area dengan gradasi warna biru hingga hijau menunjukkan penyebaran pelanggan yang lebih rendah namun masih cukup signifikan. Dengan demikian, demografi pelanggan perusahaan e-commerce ini berfokus di wilayah perkotaan Brasil bagian tenggara, yang mencakup kota-kota besar seperti São Paulo, Rio de Janeiro, dan sekitarnya.')


elif analysis_type == "Produk Terbaik":
    # Validasi Input Tanggal
    st.markdown("## 📊 Produk Terbaik Berdasarkan Periode")
    if start_date > end_date:
        with st.spinner('Sedang memuat data...'):
            time.sleep(1)
        st.error("❌ Error: Tanggal mulai harus lebih kecil dari tanggal akhir.")
    else:
        with st.spinner('Sedang memuat data...'):
            # Filter Data
            filtered_data = odr_itm_paymnt_timestmp_df[(odr_itm_paymnt_timestmp_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & (odr_itm_paymnt_timestmp_df['order_purchase_timestamp'] <= pd.to_datetime(end_date))]
            best_productid_revenue_df = filtered_data.groupby('product_id')['payment_value'].sum().reset_index()
        
            productname_revenue_df = load_productname_revenue(best_productid_revenue_df)
            productname_eng_revenue_df = load_productname_eng_revenue(productname_revenue_df)
        
            # Meggunakan 10 produk yang menghasilkan revenue terbesar
            top_products = productname_eng_revenue_df.sort_values(by='payment_value', ascending=False).head(10)
            # Agar visualisasi dimulai dari product dengan revenue terkecil dahulu
            top_products = top_products.sort_values(by='payment_value', ascending=True)
        
            # Visualisasi Bar Chart
            st.markdown(f"#### 📈 Grafik Produk Terbaik dari **{start_date}** hingga **{end_date}**")
            if not filtered_data.empty:
                plt.figure(figsize=(10, 6))
                sns.barplot(x='product_id', y='payment_value', data=top_products, hue='product_id', palette='crest', errorbar=None)
                plt.xticks(ticks=top_products['product_id'], labels=top_products['product_category_name_english'], rotation=45)
                plt.xlabel('Product Name')
                plt.ylabel('Payment Value')
                plt.title('Top 10 Products by Payment Value')
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.warning("⚠️ Tidak ada data untuk rentang tanggal yang dipilih.")
                
        st.success("✅ Data berhasil dimuat!")

elif analysis_type == "Analisis RFM":
    # Validasi Input Tanggal
    st.markdown("## 📊 Pelanggan Terbaik untuk Setiap Kriteria RFM")
    if start_date > end_date:
        with st.spinner('Sedang memuat data...'):
            time.sleep(1)
        st.error("❌ Error: Tanggal mulai harus lebih kecil dari tanggal akhir.")
    else:
        with st.spinner('Sedang memuat data...'):
            filtered_data = order_with_payments_df[(order_with_payments_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & (order_with_payments_df['order_purchase_timestamp'] <= pd.to_datetime(end_date))]
        
            customer_order_count = load_cust_order_count(filtered_data)
            customer_total_payments = load_cust_total_payment(filtered_data)
        
            # Recency
            filtered_data['days_since_last_order'] = (datetime.now() - filtered_data['order_purchase_timestamp']).dt.days
            top10_recency = filtered_data.sort_values(by='days_since_last_order', ascending=True).head(10)
            # Agar visualisasi dimulai dari customer dengan recency terbesar dahulu
            top10_recency = top10_recency.sort_values(by='days_since_last_order', ascending=False)
        
            # Frequency
            top10_frequency = customer_order_count.sort_values(by='order_count', ascending=False).head(10)
            top10_frequency = top10_frequency.sort_values(by='order_count', ascending=True)

            # Monetary
            top10_monetary = customer_total_payments.sort_values(by='total_payment', ascending=False).head(10)
            top10_monetary = top10_monetary.sort_values(by='total_payment', ascending=True)
        
            # Visualisasi Bar Chart
            st.markdown(f"#### 📈 Grafik Pelanggan Terbaik Berdasarkan Analisis RFM dari **{start_date}** hingga **{end_date}**")
            if not filtered_data.empty:
                fig, axes = plt.subplots(1, 3, figsize=(18, 6))

                sns.barplot(ax=axes[0], x='customer_id', y='days_since_last_order', data=top10_recency, hue='customer_id', palette='Blues')
                axes[0].set_xticks(range(len(top10_recency)))
                axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90) 
                axes[0].set_title('Top 10 Pelanggan Berdasarkan Recency')

                sns.barplot(ax=axes[1], x='customer_id', y='order_count', data=top10_frequency, hue='customer_id', palette='Oranges')
                axes[1].set_xticks(range(len(top10_frequency)))
                axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90) 
                axes[1].set_title('Top 10 Pelanggan Berdasarkan Frequency')

                sns.barplot(ax=axes[2], x='customer_id', y='total_payment', data=top10_monetary, hue='customer_id', palette='Greens')
                axes[2].set_xticks(range(len(top10_monetary))) 
                axes[2].set_xticklabels(axes[2].get_xticklabels(), rotation=90)  
                axes[2].set_title('Top 10 Pelanggan Berdasarkan Monetary')

                plt.tight_layout()
                st.pyplot(plt)
                
            else:
                st.warning("⚠️ Tidak ada data untuk rentang tanggal yang dipilih.")

        st.success("✅ Data berhasil dimuat!")
