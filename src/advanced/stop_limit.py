import argparse
import os
from dotenv import load_dotenv
from binance import Client
from binance.enums import ORDER_TYPE_STOP, TIME_IN_FORCE_GTC
import logging

# Setup
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

parser = argparse.ArgumentParser(description="Place a Stop-Limit Order on Binance Futures Testnet")
parser.add_argument("symbol", help="Trading pair like BTCUSDT")
parser.add_argument("side", help="BUY or SELL")
parser.add_argument("quantity", type=float, help="Amount to trade")
parser.add_argument("stop_price", type=float, help="Stop price to trigger limit order")
parser.add_argument("limit_price", type=float, help="Limit price once stop is hit")

args = parser.parse_args()

# Initialize client
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binancefuture.com/fapi'

# Place Stop-Limit Order
try:
    order = client.futures_create_order(
        symbol=args.symbol.upper(),
        side=args.side.upper(),
        type=ORDER_TYPE_STOP,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=args.quantity,
        stopPrice=str(args.stop_price),
        price=str(args.limit_price),
        workingType="CONTRACT_PRICE"
    )
    logging.info(f"✅ Stop-Limit order placed: {order}")
    print("✅ Stop-Limit order placed successfully.")
    print(order)
except Exception as e:
    logging.error(f"❌ Error placing stop-limit order: {str(e)}")
    print(f"❌ Error placing stop-limit order: {str(e)}")
