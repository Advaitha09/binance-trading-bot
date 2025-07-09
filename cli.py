import json
from bot import BasicBot

def load_keys():
    with open("config.json", "r") as f:
        return json.load(f)

def main():
    print("=== Binance Futures Testnet Trading Bot ===")

    keys = load_keys()
    bot = BasicBot(keys["api_key"], keys["api_secret"], testnet=True)

    print("Order Types:\n1. Market\n2. Limit\n3. Stop-Limit")
    choice = input("Select order type (1/2/3): ").strip()

    order_type_map = {
        "1": "MARKET",
        "2": "LIMIT",
        "3":"STOP_MARKET",
        "4": "STOP"
    }

    if choice not in order_type_map:
        print("Invalid choice")
        return

    order_type = order_type_map[choice]
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter side (BUY/SELL): ").upper()
    quantity = float(input("Enter quantity: "))

    price = None
    stop_price = None

    if order_type == "LIMIT":
        price = input("Enter limit price: ")

    elif order_type in ["STOP_MARKET", "STOP"]:
        stop_price = input("Enter stop price: ")
        if order_type == "STOP":
            price = input("Enter limit price (for stop-limit execution): ")

    result = bot.place_order(symbol, side, order_type, quantity, price, stop_price)
    print("Order Result:", result)

if __name__ == "__main__":
    main()
