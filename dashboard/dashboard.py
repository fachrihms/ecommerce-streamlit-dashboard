import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import matplotlib.ticker as mticker

sns.set(style='dark')

# Load data
revenue_df = pd.read_csv("most_revenue_analyzed.csv")
payments_df = pd.read_csv("payments.csv")
recent_df = pd.read_csv("recent_purchase_analyzed_df.csv")

# Header
st.header('E-Commerce Public Dashboard')

# Visualisasi 1: Product Category With Most Revenue
# Dropdown untuk memilih kategori produk
categories = ['All'] + revenue_df['product_category_name'].unique().tolist()
selected_category = st.selectbox("Select Product Category", categories, key="viz1")

# Hitung total revenue berdasarkan pilihan dropdown
if selected_category != 'All':
    filtered_data = revenue_df[revenue_df['product_category_name'] == selected_category]
    total_revenue_viz1 = filtered_data['price'].sum()
else:
    total_revenue_viz1 = revenue_df['price'].sum()

# Kolom untuk subheader dan total revenue
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Product Category With Most Revenue")
with col2:
    st.write(f"**Total Revenue**: USD{total_revenue_viz1:,.2f}")

# Data untuk visualisasi
revenue_grouped = revenue_df.groupby('product_category_name')['price'].sum().sort_values(ascending=False)

# Warna dinamis untuk highlight
if selected_category != 'All':
    colors = ['orange' if category == selected_category else 'lightgray' for category in revenue_grouped.index]
else:
    # Warna default matplotlib untuk All
    default_colors = [color['color'] for color in plt.rcParams['axes.prop_cycle']]
    colors = default_colors[:len(revenue_grouped)]

# Plot Bar Chart
fig1, ax1 = plt.subplots()
revenue_grouped.plot(kind='bar', color=colors, ax=ax1, edgecolor='black')
ax1.set_title("Product Category With Most Revenue")
ax1.set_xlabel("Product Category Name")
ax1.set_ylabel("Total Revenue")
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig1)


# Dropdown menu for payment method selection
payment_methods = ['All'] + payments_df['payment_type'].unique().tolist()
selected_payment = st.selectbox("Select Payment Method to Highlight:", payment_methods)

# Visualisasi 2: Most Transaction Through Payment Method
st.subheader("Most Transaction Through Payment Method")
payments_grouped = payments_df.groupby('payment_type')['transaction_count'].sum()
colors = (
    ['orange' if method == selected_payment else 'lightgray' for method in payments_grouped.index]
    if selected_payment != 'All' else plt.cm.Paired.colors[:len(payments_grouped)]
)
fig2, ax2 = plt.subplots()
ax2.pie(payments_grouped, labels=payments_grouped.index, autopct='%1.1f%%', startangle=90, colors=colors)
ax2.set_title("Most Transaction Through Payment Method")
st.pyplot(fig2)

# Visualisasi 3: Most Valuable Payment Method
if selected_payment != 'All':
    # Filter data sesuai metode pembayaran yang dipilih
    filtered_data = payments_df[payments_df['payment_type'] == selected_payment]
    total_revenue_viz3 = filtered_data['payment_value'].sum()
else:
    # Gunakan seluruh data untuk "All"
    total_revenue_viz3 = payments_df['payment_value'].sum()

# Kolom untuk subheader dan total revenue
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Most Valuable Payment Method")
with col2:
    st.write(f"**Total Revenue**: USD{total_revenue_viz3:,.2f}")

# Data untuk visualisasi
payment_value_grouped = payments_df.groupby('payment_type')['payment_value'].sum().sort_values(ascending=True)

# Warna dinamis untuk highlight
if selected_payment != 'All':
    colors = ['orange' if method == selected_payment else 'lightgray' for method in payment_value_grouped.index]
else:
    # Warna default matplotlib untuk All
    default_colors = [color['color'] for color in plt.rcParams['axes.prop_cycle']]
    colors = default_colors[:len(payment_value_grouped)]

# Plot Horizontal Bar Chart
fig3, ax3 = plt.subplots()
payment_value_grouped.plot(kind='barh', color=colors, ax=ax3, edgecolor='black')
ax3.set_title("Most Valuable Payment Method")
ax3.set_xlabel("Total Payment Value")
ax3.set_ylabel("Payment Type")
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{int(y):,}'))
st.pyplot(fig3)

# Visualisasi 4: Most Recently Purchased Product Category
st.subheader("Most Recently Purchased Product Category (2017-2018)")
top5_recent = recent_df[['product_category_name', 'product_id']].head(5)
fig4 = plt.figure(figsize=(10, 5))
sns.barplot(
    y="product_id",
    x="product_category_name",
    data=top5_recent,
    color="orange"
)
plt.title("Most Recently Purchased Product Category (2017-2018)", loc="center", fontsize=15)
plt.ylabel("Number of Products Purchased")
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
st.pyplot(fig4)

# Footer
st.caption('Copyright (c) Fachri 2025')
