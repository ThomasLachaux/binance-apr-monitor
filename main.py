import requests
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from os import environ


def get_price(coin):
    response = requests.get(
        f"https://www.binance.com/bapi/earn/v1/public/lending/daily/product/market-apr/List?productId={coin}"
    )
    response.raise_for_status()

    prices = response.json()["data"]

    for price in prices:
        yield f"flexible_apy,asset={price['asset']} apr={float(price['marketApr'])} {int(price['calcTime'])}000000"


with InfluxDBClient(
    url=environ["INFLUXDB_URL"],
    token=environ["INFLUXDB_TOKEN"],
) as client:
    bucket = environ["INFLUXDB_BUCKET"]
    org = environ["INFLUXDB_ORG"]

    with client.write_api(write_options=SYNCHRONOUS) as api:
        for price in get_price("BTC001"):
            print("Write price: ", price)
            api.write(bucket, org, price)
