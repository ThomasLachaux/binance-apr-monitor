import requests
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from os import environ
import time

# Sunday, January 1, 2023 12:00:00 AM
START_TIME = 1672531200000

DELTA = 4000000000

def get_price(coin, startTime, endTime):
    url = f"https://www.binance.com/bapi/earn/v1/public/lending/daily/product/market-apr/List?productId={coin}"

    if startTime:
        url += f"&startTime={startTime}"
    
    if endTime:
        url += f"&endTime={endTime}"

    print("Request URL: ", url)
    response = requests.get(url)
    response.raise_for_status()

    prices = response.json()["data"]

    return_prices = []

    for price in prices:
        return_prices.append(f"flexible_apy,asset={price['asset']} apr={float(price['marketApr'])} {int(price['calcTime'])}000000")
    return return_prices


with InfluxDBClient(
    url=environ["INFLUXDB_URL"],
    token=environ["INFLUXDB_TOKEN"],
) as client:
    bucket = environ["INFLUXDB_BUCKET"]
    org = environ["INFLUXDB_ORG"]

    with client.write_api(write_options=SYNCHRONOUS) as api:

        for coin in environ['COINS'].split(','):
            print("Coin: ", coin)
            startTime = START_TIME
            while startTime < time.time() * 1000:
                endTime = startTime + DELTA

                prices = get_price(coin, startTime, endTime)
                
                for price in prices:
                    print("Write price: ", price)
                    api.write(bucket, org, price)

                startTime = endTime