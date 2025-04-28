import pymongo
import config
import alpaca_trade_api as tradeapi
import datetime

def create_mongo_client():
    """Creates a MongoDB client."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['alpaca_data']  # Your MongoDB database
    collection = db['candlestick_data']  # MongoDB collection for the data
    return collection

def create_api():
    """Creates an Alpaca API instance."""
    api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.BASE_URL)
    return api

def get_bars(symbol, time_frame='day', limit=100):
    """Fetch bars (candlestick data) for a given symbol."""
    api = create_api()
    bars = api.get_barset(symbol, time_frame, limit=limit)
    return bars[symbol]

def store_data_in_mongo(data):
    """Store the fetched data in MongoDB."""
    collection = create_mongo_client()
    collection.insert_many(data)  # Insert data into MongoDB collection

def fetch_and_store_data(symbol):
    """Fetch Alpaca data and store it in MongoDB."""
    bars = get_bars(symbol)
    data_to_store = []
    for bar in bars:
        bar_data = {
            'symbol': symbol,
            'time': bar.t,
            'open': bar.o,
            'close': bar.c,
            'high': bar.h,
            'low': bar.l,
            'volume': bar.v
        }
        data_to_store.append(bar_data)
    store_data_in_mongo(data_to_store)

if __name__ == '__main__':
    # Example: Fetch and store AAPL data in MongoDB
    fetch_and_store_data('AAPL')
    print("Data successfully fetched and stored in MongoDB!")