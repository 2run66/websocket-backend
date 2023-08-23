import asyncio
import json
import websockets
import requests

PORT = 8080  # Websocket port


def get_order_book(symbol, limit):
    base_url = 'https://api.binance.com/api/v3/depth'
    params = {
        "symbol": symbol,
        "limit": limit
    }
    response = requests.get(base_url, params)  # Send request to Binance
    if response.status_code == 200:
        order_book_data = response.json()
        formatted_bids = [[float(format(float(price), '.2f')), float(format(float(quantity), '.2f'))] for price, quantity in order_book_data['bids']]
        formatted_asks = [[float(format(float(price), '.2f')), float(format(float(quantity), '.2f'))] for price, quantity in order_book_data['asks']]
        formatted_order_book_data = {
            'lastUpdateId': order_book_data['lastUpdateId'],
            'bids': formatted_bids,
            'asks': formatted_asks
        }

        data = json.dumps(formatted_order_book_data)
        return data
    else:
        return None


async def echo(websocket, path):
    last_response = {}
    while True:
        try:
            req = await websocket.recv()  # Get symbol and limit from client
            data = json.loads(req)
            symbol = data["symbol"]
            limit = data["limit"]
            data = get_order_book(symbol, limit)  # Get orderbook data from Binance
            last_response = data
            await websocket.send(data)  # Send fetched data to the client
            await asyncio.sleep(1)  # Send data every 5 seconds
        except:
            websocket.send(last_response)


if __name__ == "__main__":
    start_server = websockets.serve(echo, 'localhost', PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
