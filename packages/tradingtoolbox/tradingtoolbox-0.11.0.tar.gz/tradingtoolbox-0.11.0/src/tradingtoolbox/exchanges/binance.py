from binance.client import Client
from enum import Enum
import pandas as pd
import os


class Timeframes(Enum):
    TF_12HOUR = Client.KLINE_INTERVAL_12HOUR
    TF_1DAY = Client.KLINE_INTERVAL_1DAY
    TF_1HOUR = Client.KLINE_INTERVAL_1HOUR
    TF_1MINUTE = Client.KLINE_INTERVAL_1MINUTE
    TF_1WEEK = Client.KLINE_INTERVAL_1WEEK
    TF_1MONTH = Client.KLINE_INTERVAL_1MONTH
    TF_2HOUR = Client.KLINE_INTERVAL_2HOUR
    TF_30MINUTE = Client.KLINE_INTERVAL_30MINUTE
    TF_3DAY = Client.KLINE_INTERVAL_3DAY
    TF_3MINUTE = Client.KLINE_INTERVAL_3MINUTE
    TF_4HOUR = Client.KLINE_INTERVAL_4HOUR
    TF_5MINUTE = Client.KLINE_INTERVAL_5MINUTE
    TF_6HOUR = Client.KLINE_INTERVAL_6HOUR
    TF_8HOUR = Client.KLINE_INTERVAL_8HOUR

    def __str__(self):
        return self.value


class Binance:
    def __init__(self):
        self.client = Client()

    def create_binance_dataframe(self, klines):
        df = pd.DataFrame(
            klines,
            dtype=float,
            columns=(
                "Open Time",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Close time",
                "Quote asset volume",
                "Number of trades",
                "Taker buy base asset volume",
                "Taker buy quote asset volume",
                "Ignore",
            ),
        )

        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
        df.drop(
            columns=[
                "Close time",
                "Quote asset volume",
                "Number of trades",
                "Taker buy base asset volume",
                "Taker buy quote asset volume",
                "Ignore",
            ],
            inplace=True,
        )
        # Rename columns using a dictionary
        new_column_names = {
            "Open Time": "Date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
        df = df.rename(columns=new_column_names)
        df.set_index("Date", inplace=True)

        return df

    def get_futures_klines(self, tf, asset="BTCUSDT", ago="1 day ago UTC", cache=True):
        file = f"./data/binance_futures_{asset}_{tf}_klines.parquet"
        if cache:
            if os.path.exists(file):
                df = pd.read_parquet(file)
                return df
        klines = self.client.futures_historical_klines(asset, tf, ago)

        df = self.create_binance_dataframe(klines)
        df.to_parquet(file)
        return df

    def get_klines(self, tf, asset="BTCUSDT", ago="1 day ago UTC", cache=True):
        file = f"./data/binance_spot_{asset}_{tf}_klines.parquet"
        if cache:
            if os.path.exists(file):
                df = pd.read_parquet(file)
                return df
        klines = self.client.get_historical_klines(asset, tf, ago)

        df = self.create_binance_dataframe(klines)
        df.to_parquet(file)
        return df


binance = Binance()
