import streamlit as st

def display_emissions_trading():
    st.header("Carbon Credits Trading")
    
    sellers_df = st.session_state.buildings_data[
        st.session_state.buildings_data['credits_available'] > 0
    ][['name', 'credits_available', 'price_per_credit']]
    
    if not sellers_df.empty:
        st.subheader("Available Credits")
        st.dataframe(sellers_df)
        
        # Credit purchase form
        st.subheader("Purchase Credits")
        buyer = st.selectbox("Select Your Building", options=st.session_state.buildings_data['name'])
        seller = st.selectbox("Select Seller", options=sellers_df['name'])
        credits_to_buy = st.number_input(
            "Number of Credits to Purchase",
            min_value=1,
            max_value=int(sellers_df[sellers_df['name'] == seller]['credits_available'].iloc[0])
        )
        
        if st.button("Purchase Credits"):
            st.success(f"Successfully purchased {credits_to_buy:,} credits from {seller}")
