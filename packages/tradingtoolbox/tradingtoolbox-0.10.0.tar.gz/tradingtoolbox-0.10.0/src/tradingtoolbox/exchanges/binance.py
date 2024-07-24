from binance.client import Client
import pandas as pd
import os


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
