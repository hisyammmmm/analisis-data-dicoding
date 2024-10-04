import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.write(
    """
    # Analisis Data E-Commerce Public Dataset
            Project Akhir Analisis Data dengan Python
    """
)

orders_df = pd.read_csv('orders_dataset.csv')
products_df = pd.read_csv('products_dataset.csv')
order_items_df = pd.read_csv('order_items_dataset.csv')
order_reviews_df = pd.read_csv('order_reviews_dataset.csv')
product_category_name_translation_df = pd.read_csv('product_category_name_translation.csv')

st.subheader("Produk dengan kategori apa yang memiliki penjualan tertinggi pada tahun 2017")
merged_df = pd.merge(order_items_df, products_df[['product_id', 'product_category_name']], on='product_id')
merged_df = pd.merge(merged_df, orders_df[['order_id', 'order_purchase_timestamp']], on='order_id')
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'], errors='coerce')
merged_df = merged_df.dropna(subset=['order_purchase_timestamp'])
merged_df_2017 = merged_df[merged_df['order_purchase_timestamp'].dt.year == 2017]
most_ordered_categories = merged_df_2017['product_category_name'].value_counts().head(10)

fig, ax = plt.subplots()
most_ordered_categories.plot(kind='bar', color='skyblue', ax=ax)
plt.title('Top 10 Most Ordered Product Categories in 2017')
plt.xlabel('Product Category')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Apa saja kategori produk 10 teratas yang memiliki rating di atas 4 pada tahun 2017, dan bagaimana distribusinya berdasarkan kategori produk untuk membantu kita menentukan prioritas peningkatan kualitas?")
merged_df = pd.merge(order_items_df, products_df[['product_id', 'product_category_name']], on='product_id')
merged_df = pd.merge(merged_df, order_reviews_df[['order_id', 'review_score']], on='order_id')
merged_df = pd.merge(merged_df, orders_df[['order_id', 'order_purchase_timestamp']], on='order_id')
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'], errors='coerce')
merged_df = merged_df.dropna(subset=['order_purchase_timestamp'])
merged_df_2017 = merged_df[merged_df['order_purchase_timestamp'].dt.year == 2017]
high_rated_products = merged_df_2017[merged_df_2017['review_score'] > 4]
category_distribution = high_rated_products['product_category_name'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(12, 8))
category_distribution.plot(kind='bar', color='lightcoral', ax=ax)
plt.title('Top 10 Products with Rating Above 4 in 2017 by Product Category', fontsize=16)
plt.xlabel('Product Category', fontsize=14)
plt.ylabel('Number of Products', fontsize=14)
plt.xticks(rotation=30, ha='right', fontsize=12)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Analisis RFM")
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
analysis_date = pd.Timestamp('2024-10-04')
merged_df = pd.merge(orders_df, order_items_df[['order_id', 'price']], on='order_id')

rfm_df = merged_df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (analysis_date - x.max()).days,  # Recency
    'order_id': 'count',
    'price': 'sum'
}).rename(columns={
    'order_purchase_timestamp': 'Recency',
    'order_id': 'Frequency',
    'price': 'Monetary'
}).reset_index()

st.subheader("RFM Data")
st.dataframe(rfm_df)

def plot_rfm_bar(rfm_df, metric):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='customer_id', y=metric, data=rfm_df.sort_values(metric, ascending=False).head(10), ax=ax)
    plt.title(f'Top 10 Customers by {metric}')
    plt.xlabel('Customer ID')
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

plot_rfm_bar(rfm_df, 'Recency')
plot_rfm_bar(rfm_df, 'Frequency')
plot_rfm_bar(rfm_df, 'Monetary')



st.title('Conclusion')
tab1, tab2, tab3 = st.tabs(["Q1", "Q2", "RFM"])
 
with tab1:
    st.write(
    """
    ### Produk dengan kategori apa yang memiliki penjualan tertinggi pada tahun 2017?
    Kategori Produk Paling Laku: Analisis menunjukkan bahwa kategori produk tertentu memiliki tingkat penjualan yang signifikan pada tahun 2017. Kategori ini dapat digunakan untuk mengarahkan strategi pemasaran dan pengembangan produk. Mengidentifikasi kategori paling laku membantu perusahaan dalam merencanakan stok dan kampanye promosi yang lebih efektif, yang pada gilirannya dapat meningkatkan profitabilitas.
    """
)
 
with tab2:
    st.write(
    """
    ### Apa saja kategori produk 10 teratas yang memiliki rating di atas 4 pada tahun 2017, dan bagaimana distribusinya berdasarkan kategori produk untuk membantu kita menentukan prioritas peningkatan kualitas?
    Produk dengan Rating di Atas 4: Hasil analisis mengungkapkan bahwa ada sejumlah produk yang mendapatkan rating tinggi, mencerminkan kualitas dan kepuasan pelanggan. Distribusi produk berkualitas tinggi berdasarkan kategori memberikan wawasan tentang area kekuatan dan peluang untuk perbaikan. Fokus pada produk dengan rating tinggi dapat memperkuat brand loyalty dan mendorong penjualan lebih lanjut.
    """
)
 
with tab3:
    st.write(
    """
    ### Analisis RFM
    Analisis RFM mengungkapkan wawasan penting tentang perilaku pelanggan. Dengan membagi pelanggan berdasarkan Recency, Frequency, dan Monetary, perusahaan dapat mengidentifikasi segmen pelanggan yang paling berharga dan merancang strategi pemasaran yang ditargetkan. Recency menunjukkan kapan terakhir kali pelanggan melakukan pembelian, membantu mengidentifikasi pelanggan yang mungkin perlu dipicu untuk kembali bertransaksi. Frequency mengindikasikan seberapa sering pelanggan melakukan pembelian, yang berguna untuk merangsang pembelian ulang. Monetary memberikan informasi tentang total pengeluaran, yang menunjukkan pelanggan dengan potensi pengeluaran tertinggi.
    """
)