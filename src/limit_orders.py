import argparse
import os
from dotenv import load_dotenv
from binance import Client
from binance.enums import ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
import logging

# Load API credentials
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Configure logging
logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# CLI arguments
parser = argparse.ArgumentParser(description="Place a Binance Futures Limit Order")
parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
parser.add_argument("side", help="BUY or SELL")
parser.add_argument("quantity", type=float, help="Quantity to trade")
parser.add_argument("price", type=float, help="Limit price")
args = parser.parse_args()

# Initialize client
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binancefuture.com/fapi'

# Place limit order
try:
    order = client.futures_create_order(
        symbol=args.symbol.upper(),
        side=args.side.upper(),
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=args.quantity,
        price=str(args.price)
    )
    logging.info(f"✅ Limit order placed: {order}")
    print("✅ Limit order placed successfully.")
    print(order)
except Exception as e:
    logging.error(f"❌ Binance API Error: {str(e)}")
    print(f"❌ Error placing limit order: {str(e)}")
