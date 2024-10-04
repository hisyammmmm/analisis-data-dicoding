import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Judul Halaman
st.write(
    """
    # Analisis Data E-Commerce Public Dataset
    Project Akhir Analisis Data dengan Python
    """
)

# Load the combined dataset (all_data.csv)
all_data_df = pd.read_csv('all_data.csv')

# Bagian 1: Kategori produk dengan penjualan tertinggi pada tahun 2017
st.subheader("Produk dengan kategori apa yang memiliki penjualan tertinggi pada tahun 2017?")

# Konversi kolom tanggal
all_data_df['order_purchase_timestamp'] = pd.to_datetime(all_data_df['order_purchase_timestamp'], errors='coerce')

# Drop NaN dari kolom yang penting
all_data_df = all_data_df.dropna(subset=['order_purchase_timestamp'])

# Filter data tahun 2017
all_data_2017 = all_data_df[all_data_df['order_purchase_timestamp'].dt.year == 2017]

# Top 10 kategori produk terlaris tahun 2017
most_ordered_categories = all_data_2017['product_category_name'].value_counts().head(10)

# Visualisasi dengan barplot
fig, ax = plt.subplots()
most_ordered_categories.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title('Top 10 Most Ordered Product Categories in 2017')
ax.set_xlabel('Product Category')
ax.set_ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Bagian 2: Produk dengan rating di atas 4 pada tahun 2017
st.subheader("10 Kategori produk teratas dengan rating di atas 4 pada tahun 2017")

# Filter produk dengan review_score > 4
high_rated_products = all_data_2017[all_data_2017['review_score'] > 4]

# Distribusi kategori produk dengan rating di atas 4
category_distribution = high_rated_products['product_category_name_english'].value_counts().head(10)

# Visualisasi kategori produk dengan rating > 4
fig, ax = plt.subplots(figsize=(12, 8))
category_distribution.plot(kind='bar', color='lightcoral', ax=ax)
ax.set_title('Top 10 Products with Rating Above 4 in 2017 by Product Category', fontsize=16)
ax.set_xlabel('Product Category (English)', fontsize=14)
ax.set_ylabel('Number of Products', fontsize=14)
plt.xticks(rotation=30, ha='right', fontsize=12)
plt.tight_layout()
st.pyplot(fig)

# Bagian 3: Analisis RFM
st.subheader("Analisis RFM (Recency, Frequency, Monetary)")

# Menentukan tanggal analisis
analysis_date = pd.Timestamp('2024-10-04')

# Membuat dataframe RFM
rfm_df = all_data_df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (analysis_date - x.max()).days,  # Recency
    'order_id': 'count',  # Frequency
    'price': 'sum'  # Monetary
}).rename(columns={
    'order_purchase_timestamp': 'Recency',
    'order_id': 'Frequency',
    'price': 'Monetary'
}).reset_index()

# Menampilkan data RFM di dashboard
st.subheader("Data RFM Pelanggan")
st.dataframe(rfm_df)

# Fungsi untuk menampilkan bar plot RFM
def plot_rfm(metric):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='customer_id', y=metric, data=rfm_df.sort_values(metric, ascending=False).head(10), ax=ax)
    ax.set_title(f'Top 10 Customers by {metric}')
    ax.set_xlabel('Customer ID')
    ax.set_ylabel(metric)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Plot RFM untuk Recency, Frequency, dan Monetary
plot_rfm('Recency')
plot_rfm('Frequency')
plot_rfm('Monetary')

# Kesimpulan
st.title('Conclusion')
tab1, tab2, tab3 = st.tabs(["Q1", "Q2", "RFM"])

with tab1:
    st.write(
    """
    ### Produk dengan kategori apa yang memiliki penjualan tertinggi pada tahun 2017?
    Kategori produk dengan penjualan tertinggi menunjukkan kategori yang paling diminati oleh pelanggan pada tahun 2017. Kategori ini dapat dijadikan acuan untuk strategi pemasaran dan pengelolaan stok.
    """
)

with tab2:
    st.write(
    """
    ### 10 Kategori produk teratas dengan rating di atas 4 pada tahun 2017
    Produk dengan rating tinggi mencerminkan kualitas yang baik dan kepuasan pelanggan. Fokus pada produk dengan rating tinggi dapat membantu meningkatkan loyalitas pelanggan dan reputasi brand.
    """
)

with tab3:
    st.write(
    """
    ### Analisis RFM
    Analisis RFM memungkinkan identifikasi segmen pelanggan berdasarkan perilaku pembelian. Pelanggan yang sering berbelanja (Frequency) dan baru-baru ini melakukan pembelian (Recency) adalah target ideal untuk kampanye pemasaran.
    """
)