import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Apply Custom CSS for Background and Aesthetics
st.markdown("""
    <style>
        /* ... (keep existing styles the same) ... */
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<div class="main-header">📈 Stock Market Dashboard</div>', unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("Settings")
stocks = st.sidebar.multiselect("Select Stocks", ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"], default=["AAPL"])
show_sma = st.sidebar.checkbox("Show 50-Day SMA", value=True)
show_ema = st.sidebar.checkbox("Show 20-Day EMA", value=True)
show_bollinger = st.sidebar.checkbox("Show Bollinger Bands", value=False)

# Date Range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

if start_date >= end_date:
    st.error("⚠️ Start date must be before end date.")
    st.stop()

# Initialize dictionary to store all stock data
all_stock_data = {}

for stock in stocks:
    try:
        data = yf.download(stock, start=start_date, end=end_date)
        if data.empty:
            st.warning(f"No data available for {stock} in the selected date range.")
            continue
            
        all_stock_data[stock] = data
        
        with st.container():
            st.markdown(f'<div class="stock-card">', unsafe_allow_html=True)
            st.subheader(f"Stock Data for {stock}")
            st.write(data.tail())
            
            # Plot Stock Chart
            st.subheader(f"Candlestick Chart - {stock}")
            
            fig = go.Figure(data=[go.Candlestick(x=data.index,
                                                 open=data["Open"],
                                                 high=data["High"],
                                                 low=data["Low"],
                                                 close=data["Close"],
                                                 name="Candlestick")])
            
            # Add technical indicators
            if show_sma or show_bollinger:
                data["SMA_50"] = data["Close"].rolling(window=50, min_periods=1).mean()
            if show_ema:
                data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
                
            if show_sma:
                fig.add_trace(go.Scatter(x=data.index, y=data["SMA_50"], 
                             mode="lines", name="50-Day SMA", 
                             line=dict(color="green")))
            if show_ema:
                fig.add_trace(go.Scatter(x=data.index, y=data["EMA_20"], 
                             mode="lines", name="20-Day EMA", 
                             line=dict(color="red")))
            
            # Bollinger Bands
            if show_bollinger:
                data["SMA_20"] = data["Close"].rolling(window=20, min_periods=1).mean()
                data["STD_20"] = data["Close"].rolling(window=20, min_periods=1).std()
                data["Upper_Band"] = data["SMA_20"] + (data["STD_20"] * 2)
                data["Lower_Band"] = data["SMA_20"] - (data["STD_20"] * 2)
                
                fig.add_trace(go.Scatter(x=data.index, y=data["Upper_Band"], 
                                     line=dict(color='rgba(255, 255, 255, 0.2)'), 
                                     name="Upper Band"))
                fig.add_trace(go.Scatter(x=data.index, y=data["Lower_Band"], 
                                     line=dict(color='rgba(255, 255, 255, 0.2)'), 
                                     name="Lower Band", fill='tonexty',
                                     fillcolor='rgba(100, 100, 255, 0.1)'))
            
            fig.update_layout(
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font=dict(color='white'),
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error processing {stock}: {str(e)}")

# Download CSV
if all_stock_data and st.sidebar.button("Download All Data as CSV"):
    for stock, data in all_stock_data.items():
        csv_data = data.to_csv().encode('utf-8')
        st.sidebar.download_button(
            label=f"Download {stock} CSV",
            data=csv_data,
            file_name=f"{stock}_data.csv",
            mime="text/csv"
        )
