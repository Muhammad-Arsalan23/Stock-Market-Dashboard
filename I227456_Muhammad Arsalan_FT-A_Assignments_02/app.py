import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit Page Config
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

# App Title
st.title("📈 Stock Market Dashboard")

# User Input for Stock Symbol
stocks = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]
selected_stock = st.selectbox("Select a stock:", stocks)

# Date Range Selection
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

# Fetch Stock Data
if start_date < end_date:
    stock_data = yf.download(selected_stock, start=start_date, end=end_date)

    # Display Stock Price Data
    st.subheader(f"Stock Data for {selected_stock}")
    st.write(stock_data.tail())  # Show last few rows

    # Plot Stock Price Chart
    st.subheader("Stock Price Trend")
    fig, ax = plt.subplots()
    ax.plot(stock_data["Close"], label="Closing Price", color="blue")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    st.pyplot(fig)

    # Moving Averages
    stock_data["SMA_50"] = stock_data["Close"].rolling(window=50).mean()
    stock_data["SMA_200"] = stock_data["Close"].rolling(window=200).mean()

    # Plot Moving Averages
    st.subheader("Stock Moving Averages")
    fig, ax = plt.subplots()
    ax.plot(stock_data["Close"], label="Closing Price", color="blue")
    ax.plot(stock_data["SMA_50"], label="50-Day SMA", linestyle="dashed", color="green")
    ax.plot(stock_data["SMA_200"], label="200-Day SMA", linestyle="dashed", color="red")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    st.pyplot(fig)

    # Volume Chart
    st.subheader("Trading Volume")
    fig, ax = plt.subplots()
    ax.bar(stock_data.index, stock_data["Volume"], color="purple", alpha=0.5)
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    st.pyplot(fig)

else:
    st.error("⚠️ Start date must be before end date.")

