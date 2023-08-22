import redis
import time
import asyncio
import websockets


PORT = 8080
r = redis.Redis(host="localhost", port=6379)


def get_last_data(symbol):
    current_timestamp = time.time()
    data = r.zrangebyscore(symbol, '-inf', current_timestamp)  # Get timestamped datas from redis
    data_str = data[-1].decode('utf-8')  # Get last timestamped data
    return data_str


async def echo(websocket, path):
    last_response = {}
    while True:
        try:
            params = await websocket.recv()  # Receive symbol of desired trade data
            symbol = params
            data = get_last_data(symbol)  # Get data from redis
            last_response = data
            await websocket.send(data)  # Send fetched data to the client
            await asyncio.sleep(1)  # Send data every 1 seconds
        except:
            await websocket.send(last_response)

if __name__ == "__main__":
    start_server = websockets.serve(echo, 'localhost', PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()