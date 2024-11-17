import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

# Utility Functions
def get_order_book():
    """Fetch the order book from the API."""
    response = requests.get(f"{API_BASE_URL}/order-book")
    return response.json()

def place_buy_order(quantity, price):
    """Place a buy order via the API."""
    response = requests.post(f"{API_BASE_URL}/market/buy", json={"quantity": quantity, "price": price})
    return response.json()

def place_sell_order(quantity, price):
    """Place a sell order via the API."""
    response = requests.post(f"{API_BASE_URL}/market/sell", json={"quantity": quantity, "price": price})
    return response.json()

def display_emissions_trading():
    st.header("Carbon Credits Trading Marketplace")

    # Order Book
    st.subheader("Order Book")
    order_book = get_order_book()
    if "order_book" in order_book:
        sell_orders = order_book["order_book"]["sell"]
        buy_orders = order_book["order_book"]["buy"]

        st.write("### Sell Orders")
        st.table(sell_orders)

        st.write("### Buy Orders")
        st.table(buy_orders)
    else:
        st.error("Failed to fetch order book.")

    # Buy Order Form
    st.subheader("Place a Buy Order")
    buy_quantity = st.number_input("Quantity to Buy", min_value=1, value=10, step=1, key="buy_quantity")
    buy_price = st.number_input("Price per Credit", min_value=0.1, value=1.0, step=0.1, key="buy_price")
    if st.button("Submit Buy Order"):
        buy_response = place_buy_order(buy_quantity, buy_price)
        if "error" in buy_response:
            st.error(buy_response["error"])
        else:
            st.success(f"Buy order placed successfully. Transactions: {buy_response.get('transactions', 'None')}")

    # Sell Order Form
    st.subheader("Place a Sell Order")
    sell_quantity = st.number_input("Quantity to Sell", min_value=1, value=10, step=1, key="sell_quantity")
    sell_price = st.number_input("Price per Credit", min_value=0.1, value=1.0, step=0.1, key="sell_price")
    if st.button("Submit Sell Order"):
        sell_response = place_sell_order(sell_quantity, sell_price)
        if "error" in sell_response:
            st.error(sell_response["error"])
        else:
            st.success(f"Sell order placed successfully. Transactions: {sell_response.get('transactions', 'None')}")

# Call the function to render the page
if __name__ == "__main__":
    display_emissions_trading()
