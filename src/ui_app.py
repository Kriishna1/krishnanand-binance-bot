import tkinter as tk
from tkinter import ttk, messagebox
import os
from dotenv import load_dotenv
from binance import Client
from binance.enums import ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC

# Load keys
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Init Binance Client
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binancefuture.com/fapi'

def place_order():
    symbol = symbol_entry.get().upper()
    side = side_var.get().upper()
    quantity = float(quantity_entry.get())
    order_type = order_type_var.get()

    try:
        if order_type == "Market":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
        elif order_type == "Limit":
            price = float(price_entry.get())
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=str(price)
            )
        else:
            messagebox.showerror("Unsupported", "Only Market and Limit orders are supported in UI for now.")
            return

        messagebox.showinfo("Success", f"Order placed:\n{order}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("Binance Futures Order Bot")
root.geometry("400x300")

# Order type
ttk.Label(root, text="Order Type").pack()
order_type_var = tk.StringVar(value="Market")
ttk.Combobox(root, textvariable=order_type_var, values=["Market", "Limit"]).pack()

# Side
ttk.Label(root, text="Side").pack()
side_var = tk.StringVar(value="BUY")
ttk.Combobox(root, textvariable=side_var, values=["BUY", "SELL"]).pack()

# Symbol
ttk.Label(root, text="Symbol (e.g., BTCUSDT)").pack()
symbol_entry = ttk.Entry(root)
symbol_entry.pack()

# Quantity
ttk.Label(root, text="Quantity").pack()
quantity_entry = ttk.Entry(root)
quantity_entry.pack()

# Price (optional)
ttk.Label(root, text="Price (for Limit only)").pack()
price_entry = ttk.Entry(root)
price_entry.pack()

# Submit button
ttk.Button(root, text="Place Order", command=place_order).pack(pady=10)

root.mainloop()
