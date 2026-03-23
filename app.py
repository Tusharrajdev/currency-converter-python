import streamlit as st
import requests
import time

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(page_title="Currency Converter", page_icon="💱")

# -------------------------
# CUSTOM STYLE (ANIMATION + UI)
# -------------------------

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.big-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #00f5d4;
}

.result-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #1f6f8b;
    color: white;
    text-align: center;
    font-size: 22px;
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">💱 Currency Converter</p>', unsafe_allow_html=True)

# -------------------------
# Currency List
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
# INPUT SECTION
# -------------------------

st.markdown("### 💰 Enter Amount")
amount = st.number_input("", value=1.0)

col1, col2 = st.columns(2)

with col1:
    from_currency_name = st.selectbox("From Currency", currency_names)

with col2:
    to_currency_name = st.selectbox("To Currency", currency_names)

# -------------------------
# CONVERT BUTTON
# -------------------------

if st.button("🚀 Convert Currency"):

    with st.spinner("Converting... 🔄"):
        time.sleep(1)  # animation feel

        fc = currencies[from_currency_name]
        tc = currencies[to_currency_name]

        url = f"https://api.exchangerate-api.com/v4/latest/{fc}"
        data = requests.get(url).json()

        rate = data["rates"][tc]
        result = amount * rate

        fee = result * 0.02
        final = result - fee

    # -------------------------
    # OUTPUT
    # -------------------------

    st.info(f"💡 1 {fc} = {rate:.2f} {tc}")

    st.warning(f"💳 Fee: {fee:.2f} | Final: {final:.2f} {tc}")

    st.markdown(
        f'<div class="result-box">{amount} {fc} = {result:.2f} {tc}</div>',
        unsafe_allow_html=True
    )
