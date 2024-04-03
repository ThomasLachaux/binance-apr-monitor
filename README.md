# Binance APR Monitor

This is a simple script to get APR (Annual Percentage Rate) of Binance Earn products and push it to InfluxDB.

![Binance APR Monitor](./img/grafana.jpg)

## Motivation

I want to know if the APR of Binance Earn products is really worth it. As the price can change rapidly. I may put the results in the readme later.

![Binance Earn](./img/binance.jpg)

## How to use

```
poetry install
poetry run python main.py
```

## Note

.envrc.example file is generated from .envrc using `cat .envrc | sed  's/".*"/""/g' > .envrc.example`.
