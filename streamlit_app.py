import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize connection
conn = st.connection("postgresql", type="sql")

# Query data from fact_sales
sales_info = conn.query('SELECT order_number, product_key, customer_key, order_date, shipping_date, due_date, sales_amount, quantity, price FROM gold.fact_sales limit 1000;', ttl="10m")
df_sales = pd.DataFrame(sales_info)

# Query data from dim_products
products_info = conn.query('SELECT product_key, product_id, product_number, product_name, category_id, category, subcategory, maintenance, "cost", product_line, start_date FROM gold.dim_products;', ttl="10m")
df_products = pd.DataFrame(products_info)

# Query data from dim_customers
customers_info = conn.query('SELECT customer_key, customer_id, customer_number, first_name, last_name, country, marital_status, gender, birthdate, create_date FROM gold.dim_customers;', ttl="10m")
df_customers = pd.DataFrame(customers_info)

# Set Seaborn style
sns.set(style="whitegrid")

# Explanation at the top of the Streamlit app
st.write("""
# Martech Data Warehouse Project

This Streamlit app provides visualizations and insights based on the data from the Martech Data Warehouse project. The data is organized into three layers: Bronze, Silver, and Gold, following the medallion architecture. The visualizations below showcase various aspects of the data, including customer distribution, product information, sales trends, and more.
""")

# Display images
st.image("images/what_is_data_ware_house.png", caption="Data Warehousing")
st.image("images/mar_tech_data_architecture.drawio.png", caption="Project Architecture")

st.write("""
## Data Warehousing

Data warehousing is a critical component of modern data management, enabling organizations to consolidate data from various sources, transform it into a consistent format, and make it available for analysis and reporting. The process can be likened to a well-organized kitchen where ingredients are sourced, prepared, and used to create dishes.

- **Bronze Layer**: This layer contains raw data ingested from various source systems. The data is stored in its original format without any transformations, similar to sourcing raw ingredients from different suppliers.
- **Silver Layer**: In this layer, the data is cleansed, transformed, and standardized to ensure consistency and accuracy. This is akin to preparing and organizing ingredients, making them ready for cooking.
- **Gold Layer**: The Gold layer contains the final dimension and fact tables, organized in a star schema. This layer is optimized for analytics and reporting, much like using prepared ingredients to create a finished dish that is ready to be served.
- **Data Visualizations**: The final step involves creating visualizations that provide valuable insights and make the data easy to understand, similar to presenting a well-prepared dish to customers.
""")

# Customer Distribution by Country
st.write("### Customer Distribution by Country")
fig, ax = plt.subplots()
sns.countplot(y='country', data=df_customers, hue='country', palette='viridis', ax=ax, legend=False)
ax.set_xlabel('Number of Customers')
ax.set_ylabel('Country')
st.pyplot(fig)

# Customer Distribution by Marital Status
st.write("### Customer Distribution by Marital Status")
fig, ax = plt.subplots()
df_customers['marital_status'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('viridis', len(df_customers['marital_status'].unique())), ax=ax)
ax.set_ylabel('')
st.pyplot(fig)

# Customer Age Distribution
st.write("### Customer Age Distribution")
df_customers['age'] = (pd.to_datetime('today') - pd.to_datetime(df_customers['birthdate'])).dt.days // 365
fig, ax = plt.subplots()
sns.histplot(df_customers['age'], bins=20, kde=True, color='skyblue', ax=ax)
ax.set_xlabel('Age')
st.pyplot(fig)

# Product Cost Distribution
st.write("### Product Cost Distribution")
fig, ax = plt.subplots()
sns.histplot(df_products['cost'], bins=20, kde=True, color='salmon', ax=ax)
ax.set_xlabel('Cost')
st.pyplot(fig)

# Products by Category
st.write("### Products by Category")
fig, ax = plt.subplots()
sns.countplot(y='category', data=df_products, hue='category', palette='viridis', ax=ax, legend=False)
ax.set_xlabel('Number of Products')
ax.set_ylabel('Category')
st.pyplot(fig)

# Products by Subcategory
st.write("### Products by Subcategory")
fig, ax = plt.subplots()
sns.countplot(y='subcategory', data=df_products, hue='subcategory', palette='viridis', ax=ax, legend=False)
ax.set_xlabel('Number of Products')
ax.set_ylabel('Subcategory')
st.pyplot(fig)

# Sales Amount Over Time
st.write("### Sales Amount Over Time")
fig, ax = plt.subplots()
df_sales.groupby('order_date')['sales_amount'].sum().plot(ax=ax, color='blue')
ax.set_xlabel('Order Date')
ax.set_ylabel('Sales Amount')
st.pyplot(fig)

# Quantity Sold Over Time
st.write("### Quantity Sold Over Time")
fig, ax = plt.subplots()
df_sales.groupby('order_date')['quantity'].sum().plot(ax=ax, color='green')
ax.set_xlabel('Order Date')
ax.set_ylabel('Quantity')
st.pyplot(fig)

# Sales Amount by Product
st.write("### Sales Amount by Product")
fig, ax = plt.subplots()
df_sales.groupby('product_key')['sales_amount'].sum().plot(kind='bar', ax=ax, color='purple')
ax.set_xlabel('Product Key')
ax.set_ylabel('Sales Amount')
st.pyplot(fig)

# Sales Amount by Customer
st.write("### Top 10 Distinct Sales Amounts with Customers")

# Group by customer_key and sum sales_amount
top_customers = df_sales.groupby('customer_key')['sales_amount'].sum().reset_index()

# Group by sales_amount and list customer_keys
top_sales_amounts = top_customers.groupby('sales_amount')['customer_key'].apply(list).reset_index()

# Sort by sales_amount and get top 10
top_sales_amounts = top_sales_amounts.sort_values(by='sales_amount', ascending=False).head(10)

# Plot the top 10 distinct sales amounts
fig, ax = plt.subplots()
sns.barplot(x='sales_amount', y='sales_amount', data=top_sales_amounts, palette='viridis', ax=ax, hue='sales_amount', legend=False)
ax.set_xlabel('Sales Amount')
ax.set_ylabel('Count')
ax.set_title('Top 10 Distinct Sales Amounts')
st.pyplot(fig)

# Shipping Time Analysis
st.write("### Shipping Time Analysis")
df_sales['shipping_time'] = (pd.to_datetime(df_sales['shipping_date']) - pd.to_datetime(df_sales['order_date'])).dt.days
fig, ax = plt.subplots()
sns.histplot(df_sales['shipping_time'], bins=20, kde=True, color='red', ax=ax)
ax.set_xlabel('Shipping Time (days)')
st.pyplot(fig)

# Display raw data tables
st.write("### Sample Data from fact_sales")
st.dataframe(df_sales.head(10))

st.write("### Sample Data from dim_products")
st.dataframe(df_products.head(10))

st.write("### Sample Data from dim_customers")
st.dataframe(df_customers.head(10))