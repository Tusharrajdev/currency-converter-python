import streamlit as st
import requests

st.title("💱 Currency Converter")

# -------------------------
# Full Currency List
# -------------------------

currencies = {
"United States – US Dollar (USD)": "USD",
"India – Indian Rupee (INR)": "INR",
"United Kingdom – Pound Sterling (GBP)": "GBP",
"European Union – Euro (EUR)": "EUR",
"Japan – Japanese Yen (JPY)": "JPY",
"China – Chinese Yuan (CNY)": "CNY",
"Australia – Australian Dollar (AUD)": "AUD",
"Canada – Canadian Dollar (CAD)": "CAD",
"Switzerland – Swiss Franc (CHF)": "CHF",
"Singapore – Singapore Dollar (SGD)": "SGD",
"United Arab Emirates – UAE Dirham (AED)": "AED",
"Bangladesh – Bangladeshi Taka (BDT)": "BDT",
"Pakistan – Pakistani Rupee (PKR)": "PKR",
"Nepal – Nepalese Rupee (NPR)": "NPR",
"South Africa – South African Rand (ZAR)": "ZAR",
"Saudi Arabia – Saudi Riyal (SAR)": "SAR",
"Thailand – Thai Baht (THB)": "THB",
"Turkey – Turkish Lira (TRY)": "TRY",
"Malaysia – Malaysian Ringgit (MYR)": "MYR",
"Mexico – Mexican Peso (MXN)": "MXN",
"Russia – Russian Ruble (RUB)": "RUB",
"South Korea – South Korean Won (KRW)": "KRW"
}

currency_names = list(currencies.keys())

# -------------------------
# User Input
# -------------------------

amount = st.number_input("Enter Amount", value=1.0)

from_currency_name = st.selectbox("From Currency", currency_names)
to_currency_name = st.selectbox("To Currency", currency_names)

# -------------------------
# Convert Function
# -------------------------

if st.button("Convert"):

    fc = currencies[from_currency_name]
    tc = currencies[to_currency_name]

    url = f"https://api.exchangerate-api.com/v4/latest/{fc}"
    data = requests.get(url).json()

    rate = data["rates"][tc]
    result = amount * rate

    # 💡 Today's rate
    st.info(f"💡 1 {fc} = {rate:.2f} {tc}")

    # 💳 Fee
    fee = result * 0.02
    final = result - fee

    st.warning(f"💳 Fee: {fee:.2f} | Final: {final:.2f} {tc}")

    # ✅ Result
    st.success(f"{amount} {fc} = {result:.2f} {tc}")
