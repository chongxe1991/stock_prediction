import streamlit as st
from get_stock_data_table import RawData
from plot import Stock

stock = st.text_input('Insert Stock Ticker Symbol', 'MSFT')
get_data_button = st.button("Get Fundamentals Chart")

if get_data_button:
    with st.spinner(text="Loading Chart..."):
        fig = RawData(stock).get_stock().plot()
        st.plotly_chart(fig)
