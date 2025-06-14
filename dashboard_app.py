import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Konfigurasi Halaman Streamlit (HARUS JADI YANG PERTAMA) ---
st.set_page_config(layout="wide", page_title="Superstore Sales Dashboard")

# --- Fungsi untuk Pre-processing Data ---
@st.cache_data
def load_and_preprocess_data():
    try:
        df = pd.read_csv('superstore.csv', encoding='latin-1')
    except UnicodeDecodeError:
        df = pd.read_csv('superstore.csv', encoding='cp1252')

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df.drop_duplicates(inplace=True)
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order Month Name'] = df['Order Date'].dt.month_name()

    return df

# Muat dan Pre-process data
df = load_and_preprocess_data()

# --- Bagian Judul dan Deskripsi Dashboard ---
st.title("📊 Superstore Sales Dashboard")
st.markdown("Dashboard ini menampilkan analisis penjualan dan profit dari dataset Superstore.")

# --- Bagian Sidebar untuk Filter ---
st.sidebar.header("Filter Data")

# Filter Kategori Produk
all_categories = ['All'] + list(df['Category'].unique())
selected_category = st.sidebar.selectbox(
    "Pilih Kategori Produk:",
    all_categories
)

# Terapkan Filter
filtered_df = df.copy()
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# --- Bagian Utama Dashboard ---
st.header("Ringkasan Metrik")

# Metrik Total Profit
total_profit = filtered_df['Profit'].sum()
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")

# Metrik tambahan
total_sales = filtered_df['Sales'].sum()
total_orders = filtered_df['Order ID'].nunique()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Penjualan", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Jumlah Pesanan", value=f"{total_orders:,}")


st.header("Analisis Visual")

# Visualisasi Profitabilitas per Kategori Produk
st.subheader(f"Profitabilitas per Kategori Produk ({selected_category if selected_category != 'All' else 'Semua Kategori'})")
if not filtered_df.empty:
    category_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index()
    category_profit = category_profit.sort_values(by='Profit', ascending=False)

    fig_cat_profit, ax_cat_profit = plt.subplots(figsize=(10, 6))
    sns.barplot(data=category_profit, x='Category', y='Profit', palette='viridis', ax=ax_cat_profit)
    ax_cat_profit.set_title('Profitabilitas per Kategori Produk')
    ax_cat_profit.set_xlabel('Kategori Produk')
    ax_cat_profit.set_ylabel('Total Profit')
    ax_cat_profit.tick_params(axis='x', rotation=45)
    st.pyplot(fig_cat_profit)
else:
    st.warning("Tidak ada data untuk kategori yang dipilih.")

# Visualisasi Trend Penjualan Bulanan Berdasarkan Tahun
st.subheader(f"Trend Penjualan Bulanan ({selected_category if selected_category != 'All' else 'Semua Kategori'})")
if not filtered_df.empty:
    monthly_sales = filtered_df.groupby(['Order Year', 'Order Month Name', 'Order Month'])['Sales'].sum().reset_index()
    monthly_sales = monthly_sales.sort_values(by=['Order Year', 'Order Month'])

    fig_monthly_sales, ax_monthly_sales = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=monthly_sales, x='Order Month Name', y='Sales', hue='Order Year', marker='o', ax=ax_monthly_sales)
    ax_monthly_sales.set_title('Trend Penjualan Bulanan Berdasarkan Tahun')
    ax_monthly_sales.set_xlabel('Bulan')
    ax_monthly_sales.set_ylabel('Total Penjualan')
    ax_monthly_sales.grid(True, linestyle='--', alpha=0.6)
    ax_monthly_sales.legend(title='Tahun')
    ax_monthly_sales.tick_params(axis='x', rotation=45)
    st.pyplot(fig_monthly_sales)
else:
    st.warning("Tidak ada data untuk membuat trend penjualan.")


# Informasi tambahan di footer
st.markdown("---")
st.markdown("Dibuat dengan Streamlit dan data Superstore Sales.")