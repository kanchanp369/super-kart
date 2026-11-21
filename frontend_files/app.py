# Streamlit frontend: collects inputs and calls the Flask backend
import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:7860")

st.title("SuperKart Sales Forecast")
st.write("Predict the total sales of a product in a store.")

c1, c2 = st.columns(2)
with c1:
    product_weight = st.number_input("Product Weight", 4.0, 22.0, 12.66)
    sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    area = st.number_input("Product Allocated Area", 0.004, 0.3, 0.05, format="%.3f")
    mrp = st.number_input("Product MRP", 30.0, 270.0, 150.0)
    id_char = st.selectbox("Product Id Prefix", ["FD", "DR", "NC"])
with c2:
    category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    city = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    age = st.number_input("Store Age (years)", 0, 60, 16)

payload = {
    "Product_Weight": product_weight, "Product_Sugar_Content": sugar, "Product_Allocated_Area": area,
    "Product_MRP": mrp, "Store_Size": store_size, "Store_Location_City_Type": city, "Store_Type": store_type,
    "Product_Id_char": id_char, "Store_Age_Years": age, "Product_Type_Category": category,
}

if st.button("Predict"):
    r = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=30)
    if r.ok:
        st.success(f"Predicted sales total: {r.json()['Predicted_Sales_Total']:,.2f}")
    else:
        st.error(f"Backend error: {r.status_code}")

st.divider()
st.subheader("Batch prediction")
up = st.file_uploader("Upload CSV with the model feature columns", type="csv")
if up is not None and st.button("Predict batch"):
    r = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": up.getvalue()}, timeout=60)
    st.json(r.json()) if r.ok else st.error(f"Backend error: {r.status_code}")
