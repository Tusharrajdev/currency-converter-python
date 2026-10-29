
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Tushar Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: #071629;
    color: #F3F7FF;
}
[data-testid="stSidebar"] {
    background: #081A2E;
    border-right: 1px solid #203A58;
}
.block-container {
    padding-top: 1.5rem;
    max-width: 1600px;
}
h1, h2, h3 {
    color: #F4F8FF !important;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #102B49, #0D2138);
    border: 1px solid #203F60;
    padding: 16px;
    border-radius: 14px;
}
[data-testid="stMetricLabel"] {
    color: #8FB7E7 !important;
}
[data-testid="stMetricValue"] {
    color: white !important;
}
div.stButton > button {
    background: linear-gradient(90deg, #168DE5, #713CF5);
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 43px;
    font-weight: 600;
    width: 100%;
}
div.stButton > button:hover {
    color: white;
    border: 1px solid #8FC5FF;
}
[data-testid="stDataFrame"] {
    border: 1px solid #203A58;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- CURRENCIES ----------
CURRENCIES = {
    "INR": ("Indian Rupee", "🇮🇳"),
    "USD": ("US Dollar", "🇺🇸"),
    "EUR": ("Euro", "🇪🇺"),
    "GBP": ("British Pound", "🇬🇧"),
    "JPY": ("Japanese Yen", "🇯🇵"),
    "AUD": ("Australian Dollar", "🇦🇺"),
    "CAD": ("Canadian Dollar", "🇨🇦"),
    "CHF": ("Swiss Franc", "🇨🇭"),
    "CNY": ("Chinese Yuan", "🇨🇳"),
    "AED": ("UAE Dirham", "🇦🇪"),
    "SGD": ("Singapore Dollar", "🇸🇬"),
    "NZD": ("New Zealand Dollar", "🇳🇿"),
    "BRL": ("Brazilian Real", "🇧🇷"),
    "ZAR": ("South African Rand", "🇿🇦"),
}
CODES = list(CURRENCIES.keys())
POPULAR = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF"]

# ---------- SESSION STATE ----------
defaults = {
    "converter_source": "INR",
    "converter_target": "USD",
    "converter_amount": 1000.0,
    "history": [],
    "converted": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- EXCHANGE RATE API ----------

@st.cache_data(ttl=300)
def get_rates(base):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"

    response = requests.get(url, timeout=20)
    response.raise_for_status()
    data = response.json()

    if "rates" not in data:
        raise ValueError("Exchange rate service returned invalid data.")

    updated_at = data.get("date", "Not provided")
    return data["rates"], updated_at



def swap_currencies():
    old_source = st.session_state.converter_source
    old_target = st.session_state.converter_target
    st.session_state.converter_source = old_target
    st.session_state.converter_target = old_source
    st.session_state.converted = None


def refresh_rates():
    get_rates.clear()
    st.session_state.converted = None


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🌐 Tushar Currency")
    st.caption("EXCHANGE INTELLIGENCE")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "Currency Converter",
            "Live Exchange Rates",
            "Currency Charts",
            "Conversion History",
            "Download Reports",
        ],
    )

    st.divider()
    st.info(
        "**Exchange services**\n\n"
        "Rates are supplied by an external exchange-rate provider."
    )
    st.caption("Tushar Currency Converter · Python Edition")

# ---------- HEADER ----------
header_col, date_col = st.columns([4, 1])

with header_col:
    st.caption("OVERVIEW")
    st.title(page)

with date_col:
    st.caption("TODAY")
    st.write(datetime.now().strftime("%Y-%m-%d"))

# ---------- RATE STATUS ----------
try:
    dashboard_rates, dashboard_updated = get_rates("INR")
    api_connected = True
except (requests.RequestException, ValueError, KeyError):
    dashboard_rates = {}
    dashboard_updated = "Unavailable"
    api_connected = False

# ---------- CONVERTER ----------
def converter_panel():
    st.markdown("### Currency converter")
    st.caption("Convert currencies using published exchange rates.")

    source_col, target_col = st.columns(2)

    with source_col:
        st.selectbox(
            "From currency",
            CODES,
            key="converter_source",
            format_func=lambda code:
                f"{CURRENCIES[code][1]}  {code} — {CURRENCIES[code][0]}",
        )

    with target_col:
        st.selectbox(
            "To currency",
            CODES,
            key="converter_target",
            format_func=lambda code:
                f"{CURRENCIES[code][1]}  {code} — {CURRENCIES[code][0]}",
        )

    amount_col, swap_col = st.columns([3, 1])

    with amount_col:
        st.number_input(
            "Amount to convert",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="converter_amount",
        )

    with swap_col:
        st.write("")
        st.write("")
        st.button(
            "⇄ Swap",
            key="swap_button",
            on_click=swap_currencies,
        )

    convert_col, refresh_col = st.columns([3, 1])

    with convert_col:
        convert_clicked = st.button(
            "⇄ Convert currency",
            type="primary",
            key="convert_button",
        )

    with refresh_col:
        st.button(
            "↻ Refresh rates",
            key="refresh_button",
            on_click=refresh_rates,
        )

    if convert_clicked:
        source = st.session_state.converter_source
        target = st.session_state.converter_target
        amount = st.session_state.converter_amount

        if amount <= 0:
            st.warning("Enter an amount greater than zero.")
        elif source == target:
            result = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "From": source,
                "Amount": amount,
                "To": target,
                "Rate": 1.0,
                "Converted Amount": amount,
                "Rate Update": "Same currency",
            }
            st.session_state.converted = result
            st.session_state.history.insert(0, result)
        else:
            try:
                current_rates, rate_update = get_rates(source)

                if target not in current_rates:
                    st.error("The selected target currency is unavailable.")
                    return

                # Correct calculation: amount × target rate for source base
                rate = float(current_rates[target])
                converted_amount = amount * rate

                result = {
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "From": source,
                    "Amount": amount,
                    "To": target,
                    "Rate": rate,
                    "Converted Amount": converted_amount,
                    "Rate Update": rate_update,
                }

                st.session_state.converted = result
                st.session_state.history.insert(0, result)

            except (
                requests.RequestException,
                ValueError,
                KeyError,
                TypeError,
            ) as error:
                st.error(f"Conversion failed: {error}")

    result = st.session_state.converted

    if result:
        st.divider()
        st.caption(
            f"{result['Amount']:,.2f} {result['From']} → {result['To']}"
        )

        result_col, rate_col = st.columns(2)

        result_col.metric(
            f"Converted amount ({result['To']})",
            f"{result['Converted Amount']:,.4f}",
        )

        rate_col.metric(
            "Exchange rate",
            f"1 {result['From']} = {result['Rate']:.6f} {result['To']}",
        )

        st.caption(f"Published rate update: {result['Rate Update']}")


# ---------- LIVE RATES ----------
def show_rates(base):
    try:
        current_rates, update_time = get_rates(base)

        rows = [
            {
                "Currency": code,
                "Name": CURRENCIES[code][0],
                f"Rate per 1 {base}": current_rates[code],
            }
            for code in POPULAR
            if code in current_rates
        ]

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(f"Published rate update: {update_time}")

    except (requests.RequestException, ValueError, KeyError) as error:
        st.error(f"Could not load exchange rates: {error}")


# ---------- DASHBOARD ----------
if page == "Dashboard":
    m1, m2, m3 = st.columns(3)

    m1.metric("Currency coverage", "166+", "Available currency codes")
    m2.metric(
        "Exchange rate service",
        "Connected" if api_connected else "Offline",
        "Published rates" if api_connected else "Check connection",
    )
    m3.metric(
        "Your conversions",
        len(st.session_state.history),
        "This session",
    )

    left, right = st.columns([1.75, 1])

    with left:
        st.markdown("#### QUICK TOOL")
        converter_panel()

    with right:
        st.markdown("#### CURRENCY MARKETS")
        st.markdown("### Live exchange rates")
        st.caption("Rates quoted per 1 INR")
        show_rates("INR")

    st.divider()
    st.markdown("### Currency charts")

    if api_connected:
        chart_rows = [
            {"Currency": code, "Rate": dashboard_rates[code]}
            for code in POPULAR
            if code in dashboard_rates
        ]

        if chart_rows:
            fig = px.bar(
                pd.DataFrame(chart_rows),
                x="Currency",
                y="Rate",
                title="Value of 1 INR in selected currencies",
                template="plotly_dark",
            )
            fig.update_layout(
                paper_bgcolor="#071629",
                plot_bgcolor="#0D223A",
                font_color="#F3F7FF",
            )
            st.plotly_chart(fig, use_container_width=True)

elif page == "Currency Converter":
    converter_panel()

elif page == "Live Exchange Rates":
    base = st.selectbox("Base currency", CODES, index=0)
    st.markdown(f"### Exchange rates per 1 {base}")
    show_rates(base)

elif page == "Currency Charts":
    base = st.selectbox("Chart base currency", CODES, index=0)

    try:
        chart_rates, update_time = get_rates(base)
        rows = [
            {"Currency": code, "Rate": chart_rates[code]}
            for code in CODES
            if code in chart_rates
        ]

        fig = px.bar(
            pd.DataFrame(rows),
            x="Currency",
            y="Rate",
            title=f"Exchange rates for 1 {base}",
            template="plotly_dark",
        )
        fig.update_layout(
            paper_bgcolor="#071629",
            plot_bgcolor="#0D223A",
            font_color="#F3F7FF",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Published rate update: {update_time}")

    except (requests.RequestException, ValueError, KeyError) as error:
        st.error(f"Chart data unavailable: {error}")

elif page == "Conversion History":
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        if st.button("Clear session history"):
            st.session_state.history = []
            st.session_state.converted = None
            st.rerun()
    else:
        st.info("No conversions yet. Make a conversion to see it here.")

elif page == "Download Reports":
    st.markdown("### Download conversion reports")

    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇ Download CSV report",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="tushar_currency_report.csv",
            mime="text/csv",
        )
    else:
        st.info("Your report will be available after your first conversion.")

st.divider()
st.caption(
    "Conversions use published exchange rates. The amount is indicative "
    "and may differ from rates offered by banks or payment providers."
)
