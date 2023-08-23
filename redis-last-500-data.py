import redis
import time

r = redis.Redis(host="localhost", port=6379)
current_timestamp = time.time()
symbol = 'BTCUSDT'
earliest_data = r.zrevrangebyscore(symbol, current_timestamp,min='-inf',start=0, num=10)
print(earliest_data)
print(current_timestamp)

