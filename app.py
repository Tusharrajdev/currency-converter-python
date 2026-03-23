import streamlit as st
import requests

st.title("💱 Currency Converter")

amount = st.number_input("Enter Amount", value=1.0)

from_currency = st.selectbox("From Currency", ["USD","INR","EUR","GBP","JPY"])
to_currency = st.selectbox("To Currency", ["INR","USD","EUR","GBP","JPY"])

if st.button("Convert"):

    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    data = requests.get(url).json()

    rate = data["rates"][to_currency]
    result = amount * rate

    st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")