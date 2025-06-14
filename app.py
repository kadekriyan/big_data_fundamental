import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- START: Pre-processing
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
# --- END: Pre-processing ---

print("Dataset siap untuk EDA.")

### Trend Penjualan Bulanan Berdasarkan Tahun
print("\n--- EDA: Trend Penjualan Bulanan Berdasarkan Tahun ---")
monthly_sales = df.groupby(['Order Year', 'Order Month Name', 'Order Month'])['Sales'].sum().reset_index()
monthly_sales = monthly_sales.sort_values(by=['Order Year', 'Order Month'])

plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_sales, x='Order Month Name', y='Sales', hue='Order Year', marker='o')
plt.title('Trend Penjualan Bulanan Berdasarkan Tahun', fontsize=16)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Total Penjualan', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Tahun')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()


### Profitabilitas per Kategori Produk
print("\n--- EDA: Profitabilitas per Kategori Produk ---")
category_profit = df.groupby('Category')['Profit'].sum().reset_index()
category_profit = category_profit.sort_values(by='Profit', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=category_profit, x='Category', y='Profit', palette='viridis')
plt.title('Profitabilitas per Kategori Produk', fontsize=16)
plt.xlabel('Kategori Produk', fontsize=12)
plt.ylabel('Total Profit', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()

print("\nEDA Selesai. Hasil visualisasi ditampilkan.")