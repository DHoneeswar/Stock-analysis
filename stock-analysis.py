import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def fetch_stock_data(ticker, start_date, end_date):
    """Fetch historical stock data using yfinance."""
    return yf.download(ticker, start=start_date, end=end_date)[['Close', 'Volume']]

def calculate_indicators(df):
    """Calculate 20-day SMA and Bollinger Bands."""
    df = df.dropna()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    std_dev = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['SMA_20'] + 2 * std_dev
    df['Lower_Band'] = df['SMA_20'] - 2 * std_dev
    return df.dropna()

def plot_stock_data(df, ticker):
    """Visualize stock price, indicators, and volume."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # Price and Indicators Plot
    axes[0].plot(df.index, df['Close'], label='Close Price', color='blue', linewidth=1.5)
    axes[0].plot(df.index, df['SMA_20'], label='20-Day SMA', color='orange', linestyle='dashed')
    axes[0].fill_between(df.index, df['Upper_Band'], df['Lower_Band'], color='gray', alpha=0.3)
    axes[0].set_title(f"{ticker} Stock Price with Indicators")
    axes[0].legend()
    axes[0].grid()

    # Volume Bar Plot
    axes[1].bar(df.index, df['Volume'], color='purple', alpha=0.6)
    axes[1].set_title(f"{ticker} Trading Volume")
    axes[1].grid()

    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(data_dict):
    """Plot correlation heatmap between stocks."""
    stock_prices = pd.DataFrame({ticker: data['Close'] for ticker, data in data_dict.items()})
    correlation_matrix = stock_prices.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Stock Price Correlation Heatmap")
    plt.show()

if __name__ == "__main__":
    tickers = ["AAPL", "DIS", "GOOGL"]
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch stock data in a cleaner way
    stock_data_dict = {ticker: calculate_indicators(fetch_stock_data(ticker, start_date, end_date)) for ticker in tickers}

    for ticker, data in stock_data_dict.items():
        plot_stock_data(data, ticker)

    plot_correlation_heatmap(stock_data_dict)
