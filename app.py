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

    # 💡 Show today's rate
    st.info(f"💡 1 {from_currency} = {rate:.2f} {to_currency}")

    # 💳 Fee calculation
    fee = result * 0.02
    final = result - fee

    st.warning(f"💳 Fee: {fee:.2f} | Final: {final:.2f} {to_currency}")

    # ✅ Final result
    st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
