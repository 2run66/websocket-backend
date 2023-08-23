import asyncio
import websockets
import json

async def consume_order_book():
    uri = "ws://localhost:8080"  # WebSocket server address
    async with websockets.connect(uri) as websocket:
        # Send a request for a specific symbol and limit
        request_data = {
            "symbol": "BTCUSDT",
            "limit": 10
        }

        while True:
            try:
                await websocket.send(json.dumps(request_data))
                response = await websocket.recv()
                order_book_data = json.loads(response)
                # Process and use the order book data as needed
                print(order_book_data)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(consume_order_book())
    asyncio.get_event_loop().run_forever()
