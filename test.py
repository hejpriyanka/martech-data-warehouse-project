import streamlit as st

# Initialize connection
conn = st.connection("postgresql", type="sql")



# Write a header to the data from view
st.write("### Data from the view gold.dim_customers")
customer_info = conn.query('select * from gold.dim_customers dc limit 15 ;', ttl="10m")
st.write(customer_info)

st.write("### Data from the view gold.dim_products")
product_info = conn.query('select * from gold.dim_products dp limit 15 ;', ttl="10m")
st.write(product_info)

st.write("### Data from the view gold.fact_sales")
sales_info = conn.query('select * from gold.fact_sales fo limit 15 ;', ttl="10m")
st.write(sales_info)


