from prefect import flow, task
from datetime import datetime
import pandas as pd
import os

from scraper.mvideo import get_price as mvideo_price


@task
def collect_data():
    data = [
        {"shop": "mvideo", "price": mvideo_price()},
    ]

    for d in data:
        d["timestamp"] = datetime.now()

    return data


@task
def save_data(data):
    df = pd.DataFrame(data)

    df.to_csv("data/raw/prices.csv", mode="a", index=False, header=not os.path.exists("data/raw/prices.csv"))


@flow
def main():
    data = collect_data()
    save_data(data)


if __name__ == "__main__":
    main()