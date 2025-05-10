# app.py

import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIG ---

GOLD_API_KEY = "YOUR_GOLD_API_KEY"  # <-- Replace with your key
GOLD_API_URL = "https://www.goldapi.io/api/XAU/INR"
SENSEX_TICKER = "^BSESN"

# --- DATA FUNCTIONS ---

def fetch_gold_prices(start_date, end_date, gold_api_key=""):
    """Fetch gold prices. If no real history available, simulate."""
    headers = {
        "x-access-token": gold_api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(GOLD_API_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Gold API Error: {response.text}")
    data = response.json()
    price = data["price"]

    dates = pd.date_range(start=start_date, end=end_date)
    prices = [price for _ in dates]
    df = pd.DataFrame({'Date': dates, 'Gold_Price': prices})
    return df.set_index('Date')

def fetch_sensex_prices(start_date, end_date):
    """Fetch Sensex historical closing prices."""
    df = yf.download(SENSEX_TICKER, start=start_date, end=end_date)
    if df.empty:
        raise Exception("Sensex data not found")
    df = df[['Close']].rename(columns={'Close': 'Sensex_Close'})
    df[['Sensex_Close']] = pd.DataFrame(df['Sensex_Close', '^BSESN'].to_list(), index=df.index)
    print(df.head())
    print(df.columns)

    return df


def prepare_combined_data(start_date, end_date):

    """Fetch and prepare combined gold and sensex data."""
    gold_df = fetch_gold_prices(start_date, end_date)
    sensex_df = fetch_sensex_prices(start_date, end_date)
    print("sensex")
    print(sensex_df.head())
    combined_df = pd.concat([gold_df, sensex_df], axis=1).dropna()
    print("hello")
    print(combined_df.columns)
    print(combined_df.head())
    combined_df['Gold_Normalized'] = normalize(combined_df, 'Gold_Price')
    print(combined_df.columns)
    combined_df['Sensex_Normalized'] = normalize(combined_df, 'Sensex_Close')
    return combined_df

def normalize(df, column_name):
    """Normalize prices to start at 100."""
    return df[column_name] / df[column_name].iloc[0] * 100

# --- STREAMLIT UI FUNCTION ---

def run_streamlit_app():
    """Streamlit UI for Gold vs Sensex comparison."""

    st.set_page_config(page_title="Gold vs Sensex Performance", layout="wide")

    st.title("📈 Gold vs Sensex - Profitability Comparison")
    st.markdown("Compare investment returns over time.")

    st.sidebar.header("Configuration")
    days = st.sidebar.selectbox("Select Period", [30, 90, 180, 365], index=1)

    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()

    try:
        combined_df = prepare_combined_data(start_date, end_date)

        # --- Plotly Graph ---
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=combined_df.index, y=combined_df['Gold_Normalized'],
                                 mode='lines', name='Gold (Normalized)'))
        fig.add_trace(go.Scatter(x=combined_df.index, y=combined_df['Sensex_Normalized'],
                                 mode='lines', name='Sensex (Normalized)'))

        fig.update_layout(title="Gold vs Sensex Performance",
                          xaxis_title="Date",
                          yaxis_title="Normalized Price (Start=100)",
                          legend=dict(x=0, y=1),
                          height=600)

        st.plotly_chart(fig, use_container_width=True)

        # --- Profitability Metrics ---
        gold_return = (combined_df['Gold_Price'].iloc[-1] / combined_df['Gold_Price'].iloc[0] - 1) * 100
        sensex_return = (combined_df['Sensex_Close'].iloc[-1] / combined_df['Sensex_Close'].iloc[0] - 1) * 100

        st.metric("Gold Return", f"{gold_return:.2f}%")
        st.metric("Sensex Return", f"{sensex_return:.2f}%")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

# --- MAIN ---

if __name__ == "__main__":
    run_streamlit_app()
