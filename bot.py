from binance.client import Client
from binance.enums import (
    SIDE_BUY,
    SIDE_SELL,
    ORDER_TYPE_MARKET,
    ORDER_TYPE_LIMIT,
    TIME_IN_FORCE_GTC
)
from logger import setup_logger

# Define STOP_MARKET manually
ORDER_TYPE_STOP_MARKET = "STOP_MARKET"
ORDER_TYPE_STOP_LIMIT = "STOP"
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = setup_logger()
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            self.client.API_URL = 'https://testnet.binancefuture.com'
        self.logger.info("Bot initialized using Binance Futures Testnet.")

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            order_params = {
                "symbol": symbol,
                "side": SIDE_BUY if side == "BUY" else SIDE_SELL,
                "type": order_type,
                "quantity": quantity,
            }

            if order_type == ORDER_TYPE_LIMIT:
                order_params["price"] = price
                order_params["timeInForce"] = TIME_IN_FORCE_GTC

            elif order_type == ORDER_TYPE_STOP_MARKET:
                order_params["stopPrice"] = stop_price
                order_params["timeInForce"] = TIME_IN_FORCE_GTC

            elif order_type == ORDER_TYPE_STOP_LIMIT:
                order_params["stopPrice"] = stop_price
                order_params["price"] = price
                order_params["timeInForce"] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**order_params)
            self.logger.info(f"Order placed: {order}")
            return order

        except Exception as e:
            self.logger.error(f"Order failed: {str(e)}")
            return {"error": str(e)}
