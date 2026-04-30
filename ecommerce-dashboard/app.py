import streamlit as st
import pandas as pd

# Configuración
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

st.title("📊 E-commerce Analytics Dashboard")
st.markdown("Análisis interactivo de ventas, clientes y comportamiento de compra")

# Cargar datos
df = pd.read_csv("../data/ecommerce_sample.csv")

# Convertir InvoiceDate a datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Crear Revenue
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# Filtro por país
country = st.selectbox("Seleccionar país", df['Country'].unique())

# Filtro por fecha
min_date = df['InvoiceDate'].min().date()
max_date = df['InvoiceDate'].max().date()

date_range = st.date_input(
    "Seleccionar rango de fechas",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Asegurarse de que siempre se selecciona un rango
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.error("Por favor, selecciona un rango de fechas válido (inicio y fin).")
    st.stop()

# Convertir a datetime para comparación

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)


# Aplicar filtros

filtered_df = df[
    (df['Country'] == country) &
    (df['InvoiceDate'] >= start_date) &
    (df['InvoiceDate'] <= end_date)
].copy()

st.write("Filas filtradas:", len(filtered_df))

# KPIs
total_revenue = filtered_df['Revenue'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
aov = filtered_df.groupby('InvoiceNo')['Revenue'].sum().mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue Total", f"${total_revenue:,.0f}")
col2.metric("🧾 Órdenes", total_orders)
col3.metric("🛒 Ticket Promedio", f"${aov:,.2f}")
# Gráfico productos
st.subheader("Top productos")

top_products = filtered_df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

st.bar_chart(top_products)

#top clientes

st.subheader("👥 Top Clientes")

top_customers = (
    filtered_df.groupby('CustomerID')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_customers)

# Ventas en el tiempo
st.subheader("Ventas en el tiempo")

sales_time = (
    filtered_df
    .resample('D', on='InvoiceDate')['Revenue']
    .sum()
    .sort_index()
)

sales_time = sales_time.fillna(0)

st.line_chart(sales_time)