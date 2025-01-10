import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import matplotlib.ticker as mticker
sns.set(style='dark')

revenue_df = pd.read_csv("most_revenue_analyzed.csv")
payments_df = pd.read_csv("payments.csv")
recent_df = pd.read_csv("recent_purchase_analyzed_df.csv")




st.header('E-Commerce Public Dashboard')
# Visualisasi 1: Product Category With Most Revenue
total_revenue_viz1 = revenue_df.groupby('product_category_name')['price'].sum().sum()

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Product Category With Most Revenue")

with col2:
    st.write(f"**Total Revenue**: USD{total_revenue_viz1:,.2f}")
revenue_grouped = revenue_df.groupby('product_category_name')['price'].sum().sort_values(ascending=False)
fig1, ax1 = plt.subplots()
revenue_grouped.plot(kind='bar', color='skyblue', ax=ax1)
ax1.set_title("Product Category With Most Revenue")
ax1.set_xlabel("Product Category Name")
ax1.set_ylabel("Total Revenue")
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig1)

# Visualisasi 2: Most Transaction Through Payment Method
st.subheader("Most Transaction Through Payment Method")
payments_grouped = payments_df.groupby('payment_type')['transaction_count'].sum()
fig2, ax2 = plt.subplots()
ax2.pie(payments_grouped, labels=payments_grouped.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax2.set_title("Most Transaction Through Payment Method")
st.pyplot(fig2)

# Visualisasi 3: Most Valuable Payment Method
total_revenue_viz3 = payments_df.groupby('payment_type')['payment_value'].sum().sum()

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Most Valuable Payment Method")
with col2:
    st.write(f"**Total Revenue**: USD{total_revenue_viz3:,.2f}")       
payment_value_grouped = payments_df.groupby('payment_type')['payment_value'].sum().sort_values(ascending=True)
fig3, ax3 = plt.subplots()
payment_value_grouped.plot(kind='barh', color='lightgreen', ax=ax3)
ax3.set_title("Most Valuable Payment Method")
ax3.set_xlabel("Total Payment Value")
ax3.set_ylabel("Payment Type")
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{int(y):,}'))
st.pyplot(fig3)

# Visualisasi 4: Most Recently Purchased Product Category
st.subheader("Most Recently Purchased Product Category (2017-2018)")

# Mengambil 5 data teratas dari revenue_df berdasarkan 'price' atau 'revenue'
top5_recent = recent_df[['product_category_name', 'product_id']].head(5)

# Plot dengan Seaborn
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

# Menampilkan plot di Streamlit
st.pyplot(fig4)

st.caption('Copyright (c) Fachri 2025')