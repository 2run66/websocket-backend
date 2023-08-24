import websocket
import json
import redis
import time


def on_message(ws, message):
    candle_data = json.loads(message)
    timestamp = time.time()
    # Format response
    if candle_data["e"] == "kline":
        candlestick = candle_data["k"]
        adapted_trade = {
            'symbol': candlestick['s'],
            'price': float(candlestick['c']),
            'volume': float(candlestick['v']),
            'timestamp': candlestick["T"]
        }
        symbol = adapted_trade["symbol"]  # Filter by symbol
        data = json.dumps(adapted_trade)
        print(data)
        r.zadd(symbol+"1m", {data: timestamp})  # Add received data to redis


def on_error(ws, error):
    print("WebSocket Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")


def on_open(ws):
    pairs = ["ethusdt@kline_1m", "btcusdt@kline_1m", "avaxusdt@kline_1m", "bnbusdt@kline_1m"]  # Set tick data pairs
    payload = {
        "method": "SUBSCRIBE",
        "params": pairs,
        "id": 1
    }
    ws.send(json.dumps(payload))  # Connect Binance socket
    print("WebSocket Opened")


if __name__ == "__main__":
    r = redis.Redis(host="localhost", port=6379)
    websocket_url = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(websocket_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
