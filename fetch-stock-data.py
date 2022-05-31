import yfinance as yf
import shutil
import os
import time
import csv

SP_FILE = "s&p500.csv"
STOCKS_LOCATION = "stocks"
MAX_API_CALLS = 1800
MAX_API_CALLS_PER = 3


def fetch_wrapper(fetch):
    time.sleep(1)
    result = fetch()
    return result


def fetch_stock_data(stocks):
    """Retrieve historic stock data to /stocks folder"""

    if os.path.isdir(STOCKS_LOCATION):
        shutil.rmtree(STOCKS_LOCATION)

    os.mkdir(STOCKS_LOCATION)

    api_calls = 0

    for i, stockmeta in enumerate(stocks):
        ticker = stockmeta["ticker"]
        api_fails = 0

        while api_fails <= MAX_API_CALLS_PER:
            api_calls += 1
            stock_location = f'{STOCKS_LOCATION}/{ticker}'
            os.mkdir(stock_location)

            try:
                stock = yf.Ticker(ticker)
                data = {
                    "history": stock.history(period="max"),
                    "recommendations": stock.recommendations,
                    "financials": stock.financials,
                    "analysis": stock.analysis
                }

                for d in data:
                    file_location = f'{stock_location}/{d}'
                    try:
                        data[d].to_csv(file_location + '.csv')
                    except AttributeError:
                        with open(file_location + '.txt', 'w') as f:
                            f.write(str(data[d]))

                with open(f'{stock_location}/_{stockmeta["name"]}.txt', 'w') as f:
                    f.write(str(stockmeta["name"]))

                time.sleep(2)
                break
            except ValueError:
                print('fail')
                api_fails += 1

        if api_fails == MAX_API_CALLS_PER:
            print("Failed to fetch", ticker)
        else:
            print(i+1, "Fetched data for", ticker)

    print("Completed fetching data for", len(stocks), "stocks")

def load_sp(sp_file=SP_FILE):
    """Load stocks from S&P 500"""
    with open(sp_file, 'r') as f:
        reader = csv.reader(f)
        stocks = [
            {"name": row[1],"ticker": row[2],}
            for row in reader
        ]
        return stocks


if __name__ == "__main__":
    stocks = load_sp()
    fetch_stock_data(stocks)
