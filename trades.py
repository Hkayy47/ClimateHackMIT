# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 03:24:05 2024

@author: Kushal
"""

import streamlit as st
import requests
import pandas as pd

# Set the Flask API base URL
FLASK_API_URL = "http://127.0.0.1:8000/api"

# Helper functions for API requests
def get_order_book():
    response = requests.get(f"{FLASK_API_URL}/order-book")
    return response.json() if response.status_code == 200 else {"order_book": {}}

def generate_sample_data(num_buildings=5):
    response = requests.post(f"{FLASK_API_URL}/generate-sample-data", json={"num_buildings": num_buildings})
    return response.json() if response.status_code == 200 else {}

def place_buy_order(quantity, price):
    response = requests.post(f"{FLASK_API_URL}/market/buy", json={"quantity": quantity, "price": price})
    return response.json()

def place_sell_order(quantity, price):
    response = requests.post(f"{FLASK_API_URL}/market/sell", json={"quantity": quantity, "price": price})
    return response.json()

# Initialize Streamlit session state
if "order_book" not in st.session_state:
    st.session_state.order_book = {}
    st.session_state.num_buildings = 5

if "sample_data_generated" not in st.session_state:
    st.session_state.sample_data_generated = False

# Sidebar for generating sample data
st.sidebar.header("Configuration")
num_buildings = st.sidebar.number_input("Number of Buildings", min_value=1, value=st.session_state.num_buildings)
if st.sidebar.button("Generate Sample Data"):
    result = generate_sample_data(num_buildings)
    st.sidebar.success("Sample data generated.")
    st.session_state.sample_data_generated = True
    st.session_state.order_book = get_order_book()["order_book"]

# Main Display
st.title("Emissions Trading Marketplace")

if not st.session_state.sample_data_generated:
    st.info("Generate sample data to start trading.")
else:
    # Display Order Book
    st.subheader("Order Book")
    buy_orders = pd.DataFrame(st.session_state.order_book.get("buy", []))
    sell_orders = pd.DataFrame(st.session_state.order_book.get("sell", []))

    if not buy_orders.empty:
        st.write("**Buy Orders**")
        st.dataframe(buy_orders)
    else:
        st.write("_No active buy orders._")

    if not sell_orders.empty:
        st.write("**Sell Orders**")
        st.dataframe(sell_orders)
    else:
        st.write("_No active sell orders._")

    # Buy Credits
    st.subheader("Buy Energy Credits")
    buy_quantity = st.number_input("Quantity to Buy", min_value=1, value=1)
    buy_price = st.number_input("Price per Credit ($)", min_value=0.1, step=0.1)
    if st.button("Place Buy Order"):
        buy_response = place_buy_order(buy_quantity, buy_price)
        st.success(buy_response["message"])
        st.session_state.order_book = get_order_book()["order_book"]

    # Sell Credits
    st.subheader("Sell Energy Credits")
    sell_quantity = st.number_input("Quantity to Sell", min_value=1, value=1)
    sell_price = st.number_input("Price per Credit ($)", min_value=0.1, step=0.1)
    if st.button("Place Sell Order"):
        sell_response = place_sell_order(sell_quantity, sell_price)
        st.success(sell_response["message"])
        st.session_state.order_book = get_order_book()["order_book"]
